"""
metrics.py - Cálculo de métricas a partir de los eventos de los clientes.

Responsables: Equipo 3 (Métricas). Revisa: Equipo 4 (UI).

Toma "eventos_clientes" (contrato de salida) y calcula el bloque "metricas":
tiempo promedio en el sistema, clientes promedio (Ley de Little), cola más
larga, utilización y tiempo ocioso por servidor, tiempo promedio de atención.
No depende de SimPy: se puede desarrollar con datos de ejemplo.
"""


def calcular_metricas(eventos_clientes: list[dict], config: dict,
                      duracion_total_minutos: float) -> dict:
    """
    Calcula las métricas del sistema completo y de cada estación.

    Args:
        eventos_clientes: un dict por cliente, con tiempo_entrada_sistema,
            tiempo_salida_sistema y la lista "paradas".
        config: la configuración usada (sirve para saber servidores y colas).
        duracion_total_minutos: duración simulada, necesaria para utilización
            y tiempo ocioso.

    Returns:
        Diccionario "metricas" con "sistema_completo" y "por_estacion",
        según docs/contratos.md.
    """
    raise NotImplementedError("Pendiente: Equipo 3 (Issues de Métricas)")
