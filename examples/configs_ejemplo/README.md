# Configuraciones de ejemplo

Cada archivo es una configuración válida según el contrato de entrada
(`docs/contratos.md`). Sirven de datos de prueba para todos los equipos.

Unidades: el tiempo se mide en **minutos**; la tasa de llegadas va en
**clientes por hora** (`lambda_por_hora`); `media`, `min` y `max` del servicio
van en minutos.

| Archivo | Método | Variante | Estado |
|---|---|---|---|
| `01_paralelo_cola_unica.json` | Paralelo | Cola única, múltiples servidores | Hecho (formato de referencia) |
| Las otras 7 variantes | | | Pendiente: Equipo 2 |

Nombres sugeridos para el resto: `02_paralelo_colas_multiples.json`,
`03_paralelo_preferencial.json`, `04_paralelo_servidor_unico.json` y
`05` a `08` con el mismo orden para Método 2 (secuencial).
