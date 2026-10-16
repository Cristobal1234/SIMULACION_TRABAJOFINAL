"""
topologias.py - Las 8 variantes de sistema de colas.

Responsables: Equipo 2 (Topologías). Revisa: Equipo 1 (Engine).

Arma configuraciones válidas (contrato de entrada) para cada combinación de
método y variante. No simula nada: eso lo hace engine.py.

Método 1 (paralelo)  x  4 variantes
Método 2 (secuencial, con triaje inicial)  x  4 variantes
"""

VARIANTES = (
    "cola_unica_multiples_servidores",
    "colas_multiples_multiples_servidores",
    "colas_multiples_preferencial_multiples_servidores",
    "colas_multiples_servidor_unico",
)


def construir_config(metodo: str, variante: str, **parametros) -> dict:
    """
    Construye una configuración completa para una variante dada.

    Args:
        metodo: "paralelo" o "secuencial".
        variante: uno de los valores de VARIANTES.
        **parametros: lambda, número de servidores y colas, distribuciones,
            proporción de clientes preferenciales, etc.

    Returns:
        Configuración que cumple el contrato de entrada (config.validar_config).
    """
    raise NotImplementedError("Pendiente: Equipo 2 (8 variantes)")
