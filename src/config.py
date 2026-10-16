"""
config.py - Contrato de entrada (configuración de la simulación).

Responsables: Equipo 2 (Topologías). Revisa: Equipo 1 (Engine).

Define qué forma tiene una configuración válida y la valida. La referencia
completa del formato está en docs/contratos.md. Si cambia la estructura del
JSON, hay que actualizar ese documento y avisar a Engine y UI.
"""

METODOS = ("paralelo", "secuencial")  # Método 1 / Método 2
DISTRIBUCIONES_SERVICIO = ("exponencial", "uniforme")
TIPOS_COLA = ("unica", "multiple", "preferencial")
REPARTICIONES = ("round_robin", "aleatoria", "mas_corta")


def validar_config(config: dict) -> list[str]:
    """
    Valida una configuración contra el contrato de entrada.

    Args:
        config: diccionario con los bloques "simulacion" y "estaciones".

    Returns:
        Lista de mensajes de error. Lista vacía si la configuración es válida.
    """
    raise NotImplementedError("Pendiente: Equipo 2 (ver docs/contratos.md)")
