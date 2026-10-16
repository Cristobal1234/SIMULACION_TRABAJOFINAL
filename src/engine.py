"""
engine.py - Motor de simulación (SimPy).

Responsables: Equipo 1 (Engine). Revisa: Equipo 2 (Topologías).

Recibe una configuración (contrato de entrada) y devuelve los eventos de cada
cliente (contrato de salida). Debe funcionar para cualquier configuración,
sin saber qué variante de topología se está simulando. Las firmas de abajo
son una propuesta inicial: Equipo 1 puede ajustarlas por PR avisando a los
equipos que las consumen.
"""


def ejecutar_simulacion(config: dict) -> dict:
    """
    Corre una simulación completa de eventos discretos.

    Args:
        config: configuración válida según el contrato de entrada
            (docs/contratos.md). Incluye la llegada Poisson única en
            config["simulacion"]["llegada"].

    Returns:
        Diccionario con "simulacion_id", "duracion_total_minutos" y la lista
        "eventos_clientes" (un registro por cliente, con sus "paradas").
        Las métricas agregadas las calcula metrics.py, no el motor.
    """
    raise NotImplementedError("Pendiente: Equipo 1 (Issues de Engine)")
