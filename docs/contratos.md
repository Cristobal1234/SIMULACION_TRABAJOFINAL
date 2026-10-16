# Contratos de datos

Todo el proyecto gira alrededor de dos estructuras JSON. Cada equipo construye
su parte sabiendo qué recibe y qué devuelve; mientras estas formas no cambien,
nadie se rompe cuando otro equipo modifica su código por dentro.

```
Config (entrada) -> Equipo 2: topologías -> Motor (Equipo 1) -> Resultado (salida)
                                                                   |-> Equipo 3: métricas
                                                                   |-> Equipo 4: interfaz
```

**Unidades:** tiempo en minutos; tasa de llegadas en clientes por hora.

**Regla de cambios:** si un PR modifica alguno de estos contratos, debe
actualizar este archivo, marcar la casilla correspondiente en la plantilla de PR
y avisar a los líderes de los equipos que lo consumen.

---

## 1. Contrato de entrada (configuración)

Los comentarios `//` son explicativos; el JSON real no los lleva.

```jsonc
{
  "simulacion": {
    "nombre": "Banco - Escenario 1",
    "metodo": "paralelo",            // "paralelo" (Método 1) | "secuencial" (Método 2)
    "duracion_minutos": 480,
    "semilla": 42,                   // reproducibilidad
    "llegada": {                     // ÚNICA frontera de entrada al sistema
      "distribucion": "poisson",
      "lambda_por_hora": 40
    }
  },

  "estaciones": [
    {
      "id": "cajeros",
      "nombre": "Atención de cajeros",
      "orden": 1,                    // solo relevante si metodo = "secuencial"

      "servidores": {
        "cantidad": 3,
        "distribucion_servicio": {
          "tipo": "exponencial",     // "exponencial" | "uniforme"
          "media": 2                 // si exponencial
          // "min": 1, "max": 2      // si uniforme
        }
      },

      "colas": {
        "cantidad": 1,               // 1 = única, >1 = múltiples
        "tipo": "unica",             // "unica" | "multiple" | "preferencial"
        "disciplina": "FIFO",
        "reparticion": null          // si "multiple": "round_robin" | "aleatoria" | "mas_corta"
      },

      "clientes_preferenciales": {
        "aplica": false,
        "proporcion": 0.0            // ej. 0.2 = 20 % son preferenciales
      },

      "siguiente_estacion": null     // id de la próxima; solo en "secuencial"
    }
  ]
}
```

### Por qué está estructurado así

- **`llegada` vive en `simulacion`, no en cada estación.** Un sistema de colas
  tiene una sola frontera de entrada al exterior. Las estaciones internas
  reciben clientes de otra estación o de la repartición entre colas; nunca
  generan su propio proceso de Poisson independiente.
- **`estaciones` es una lista.** Cubre el Método 1 (una estación con servidores
  en paralelo) y el Método 2 (varias estaciones encadenadas con
  `siguiente_estacion`) sin cambiar la forma del contrato.
- **`colas.tipo` + `colas.cantidad`** determinan las 4 combinaciones de cada
  método: única con múltiples servidores, múltiples con múltiples servidores,
  múltiples con preferencial y múltiples servidores, y múltiples con servidor
  único. El motor decide el enrutamiento leyendo solo esos dos campos.
- **`clientes_preferenciales` es un bloque autocontenido y opcional.** Las
  estaciones que no lo usan ponen `"aplica": false` y el resto lo ignora.

---

## 2. Contrato de salida (resultado)

```jsonc
{
  "resultado": {
    "simulacion_id": "banco_escenario_1",
    "duracion_total_minutos": 480,

    // DATOS CRUDOS: los produce el motor (Equipo 1). Un registro por cliente.
    "eventos_clientes": [
      {
        "cliente_id": 1,
        "es_preferencial": false,
        "tiempo_entrada_sistema": 2.3,   // único punto de entrada
        "tiempo_salida_sistema": 9.6,    // único punto de salida
        "paradas": [                     // 1 elemento en Método 1, 2 o más en Método 2
          {
            "estacion_id": "cajeros",
            "tiempo_inicio_espera": 2.3,
            "tiempo_inicio_servicio": 4.1,
            "tiempo_fin_servicio": 4.8,
            "servidor_asignado": 2,
            "cola_asignada": 1
          }
        ]
      }
    ],

    // RESUMEN: lo calcula metrics.py (Equipo 3); la interfaz solo lo muestra.
    "metricas": {
      "sistema_completo": {
        "tiempo_promedio_en_sistema": 5.2,    // promedio de (salida - entrada)
        "clientes_promedio_en_sistema": 4.1,
        "clientes_totales_atendidos": 351
      },
      "por_estacion": {
        "cajeros": {
          "tiempo_promedio_espera_cola": 1.8,
          "tiempo_promedio_atencion": 3.4,
          "longitud_promedio_cola": 2.3,
          "longitud_maxima_cola": 7,
          "por_servidor": {
            "servidor_1": {"utilizacion": 0.82, "tiempo_ocioso_minutos": 86.4, "clientes_atendidos": 118}
          },
          "por_cola": {
            "cola_1": {"longitud_promedio": 2.1, "longitud_maxima": 6}
          },
          "cola_mas_larga": "cola_1"
        }
      }
    }
  }
}
```

### Por qué está estructurado así

- **`tiempo_entrada_sistema` y `tiempo_salida_sistema` únicos por cliente.** El
  tiempo total en el sistema es `salida - entrada`, sin sumar por estación. Es
  el mismo principio del contrato de entrada: lo que pertenece al sistema
  completo se define una sola vez.
- **`paradas` es una lista que crece sola.** Con una estación tiene un elemento;
  con triaje más atención específica tiene dos. El motor no necesita lógica
  distinta por método: agrega una parada más si hay `siguiente_estacion`.
- **`eventos_clientes` es la fuente de verdad; `metricas` es el resumen.** Si
  hace falta una métrica nueva, se calcula desde los datos crudos sin tocar el
  motor. La interfaz nunca debería calcular nada: si lo necesita, falta un campo
  en `metricas`.
- **Separación `sistema_completo` / `por_estacion`.** Distingue el tiempo total
  del cliente del rendimiento de una estación, que son preguntas distintas.
  `por_servidor` responde al rendimiento y la hora ociosa; `por_cola` y
  `cola_mas_larga` responden a cuál cola es mayor.

---

## Definiciones de métricas

- **Tiempo ocioso de un servidor:** `duracion_total_minutos` menos la suma de
  minutos que estuvo atendiendo.
- **Utilización:** `tiempo_ocupado / duracion_total_minutos`.
- **Clientes promedio en el sistema:** por la Ley de Little, `L = λ · W`,
  que también se puede verificar integrando el número de clientes en el tiempo.
