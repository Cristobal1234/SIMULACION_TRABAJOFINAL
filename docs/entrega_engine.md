# Primera entrega — Equipo 1 (Engine)

## Qué se entrega

- `src/engine.py`: implementación de la firma pública y simulación SimPy.
- `tests/test_engine.py`: pruebas de contrato, FIFO, capacidad sin solapamientos,
  semilla, vaciado, distribución uniforme, ausencia de llegadas y errores.
- `examples/ejecutar_engine.py`: ejemplo completo con el JSON existente.
- `docs/contratos.md`: aclaraciones de integración y cierre de la simulación.

## Cómo ejecutarlo

Desde la carpeta principal, con Python 3.11 o superior:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest
python -m examples.ejecutar_engine
```

En Windows, activar con `.venv\Scripts\activate`.
Para guardar la salida y compartirla con UI/Métricas:

```bash
python -m examples.ejecutar_engine > resultado_engine.json
```

El ejemplo ya incluye el envoltorio `resultado`; la función del motor devuelve
solo su contenido. Las dos pruebas pendientes de otros equipos siguen omitidas.

## Cómo explicarlo en clase

1. Se lee la tasa de llegada y se convierte de clientes/hora a clientes/minuto.
2. El generador espera un intervalo exponencial y registra la llegada.
3. Cada cliente pide un servidor libre. Si no hay, espera en una cola FIFO.
4. Al conseguir servidor, registra el inicio y espera el tiempo de atención.
5. Registra la salida y devuelve el servidor para el siguiente cliente.
6. Al cerrar las llegadas se termina de atender a los pendientes y se devuelven
   los eventos. Los indicadores los calculará el equipo de Métricas.

Se usa `simpy.Store` para conservar los identificadores de los servidores
libres. Las solicitudes pendientes se atienden en FIFO. Esto permite indicar
qué servidor atendió a cada cliente, además de limitar la atención simultánea.

## Texto para comentar en el Issue de integración

Confirmamos la firma `ejecutar_simulacion(config: dict) -> dict` en
`src/engine.py`. Recibe la configuración de `docs/contratos.md` y devuelve
`simulacion_id`, `duracion_total_minutos` y `eventos_clientes`, sin envoltorio
`resultado` ni métricas. La primera entrega soporta una estación en paralelo,
cola única FIFO y varios servidores. Al cerrar las llegadas se atiende a los
pendientes; la duración total incluye ese tiempo adicional. El ejemplo se
puede ejecutar con `python -m examples.ejecutar_engine`.

## Propuesta de PR

Título: `feat(engine): implementa cola única con múltiples servidores`

El motor estaba pendiente y no permitía generar eventos para integrar los
módulos. Se implementa el caso básico de una estación con cola FIFO compartida,
llegadas Poisson y servicios exponenciales o uniformes. Se incluyen pruebas,
un ejemplo ejecutable y la documentación de la firma y de la política de cierre.

Validación: instalación de requirements y ejecución de `python -m pytest`.
Completar con el número real de tarea: `Closes #NUMERO_DEL_ISSUE`.

Para preparar el PR en el repositorio del grupo, crear una rama desde main
actualizada, copiar los cuatro archivos de esta entrega, ejecutar las pruebas,
hacer commit y subir la rama. Abrir el PR y enlazar el Issue real.
No reemplazar trabajos recientes de los demás equipos con este ZIP inicial.

Pendientes de coordinación: publicar el comentario en el Issue, abrir el PR
y entregar el enlace al líder. Esas acciones no se han realizado desde aquí.
