"""Motor SimPy: primera entrega, una estación con cola FIFO compartida."""
import math
import random
import re
import unicodedata

import simpy


def _positivo(valor, nombre):
    """Recibe un valor numérico y su nombre; devuelve el valor o lanza ValueError."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not math.isfinite(valor) or valor <= 0:
        raise ValueError(f"{nombre} debe ser un número finito mayor que cero")
    return valor


def ejecutar_simulacion(config: dict) -> dict:
    """Recibe el contrato de entrada y devuelve datos crudos sin envolver en 'resultado'.

    Primera entrega: método paralelo, una estación, cola única FIFO y uno
    o varios servidores, sin prioridad. Servicio exponencial o uniforme.
    Las llegadas se generan hasta duracion_minutos (extremo excluido).
    Después se atiende a los clientes pendientes; duracion_total_minutos
    incluye ese vaciado y nunca es menor que la ventana de llegadas.
    Una semilla fija reproduce los eventos sin alterar el generador global.
    Configuraciones incompletas o inválidas lanzan ValueError; variantes
    aún no implementadas lanzan NotImplementedError.
    """
    try:
        simulacion = config['simulacion']
        estaciones = config['estaciones']
        if simulacion['metodo'] != 'paralelo' or len(estaciones) != 1:
            raise NotImplementedError('Primera entrega: paralelo con una estación')
        estacion = estaciones[0]
        colas = estacion['colas']
        if (colas['tipo'] != 'unica' or colas['cantidad'] != 1
                or colas['disciplina'] != 'FIFO'
                or estacion.get('clientes_preferenciales', {}).get('aplica', False)
                or estacion.get('siguiente_estacion') is not None):
            raise NotImplementedError('Primera entrega: cola única FIFO sin prioridad')
        duracion = _positivo(simulacion['duracion_minutos'], 'duracion_minutos')
        llegada = simulacion['llegada']
        if llegada['distribucion'] != 'poisson':
            raise NotImplementedError('Solo se admiten llegadas Poisson')
        tasa = _positivo(llegada['lambda_por_hora'], 'lambda_por_hora') / 60
        cantidad = estacion['servidores']['cantidad']
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad < 1:
            raise ValueError('cantidad de servidores debe ser un entero positivo')
        servicio = estacion['servidores']['distribucion_servicio']
        tipo = servicio['tipo']
        if tipo == 'exponencial':
            media = _positivo(servicio['media'], 'media')
        elif tipo == 'uniforme':
            minimo = _positivo(servicio['min'], 'min')
            maximo = _positivo(servicio['max'], 'max')
            if minimo > maximo:
                raise ValueError('min no puede ser mayor que max')
        else:
            raise NotImplementedError('Servicio: exponencial o uniforme')
        estacion_id = estacion['id']
        nombre = simulacion['nombre']
        if not isinstance(nombre, str) or not isinstance(estacion_id, str) or not estacion_id:
            raise ValueError('nombre e id de estación deben ser textos; id no puede estar vacío')
        semilla = simulacion.get('semilla')
        if semilla is not None and (isinstance(semilla, bool) or not isinstance(semilla, int)):
            raise ValueError('semilla debe ser un entero o null')
    except (KeyError, TypeError, IndexError, AttributeError) as error:
        raise ValueError(f'Configuración incompleta o mal formada: {error}') from error

    azar = random.Random(semilla)
    entorno = simpy.Environment()
    # Store mantiene en FIFO a los clientes que esperan un servidor libre.
    disponibles = simpy.Store(entorno, capacity=cantidad)
    disponibles.items.extend(range(1, cantidad + 1))
    eventos = []

    def atender(cliente):
        """Recibe un evento de cliente; registra su servicio y devuelve un proceso."""
        servidor = yield disponibles.get()
        inicio = entorno.now
        tiempo = azar.expovariate(1 / media) if tipo == 'exponencial' else azar.uniform(minimo, maximo)
        yield entorno.timeout(tiempo)
        cliente['paradas'].append({
            'estacion_id': estacion_id,
            'tiempo_inicio_espera': cliente['tiempo_entrada_sistema'],
            'tiempo_inicio_servicio': inicio,
            'tiempo_fin_servicio': entorno.now,
            'servidor_asignado': servidor,
            'cola_asignada': 1,
        })
        cliente['tiempo_salida_sistema'] = entorno.now
        yield disponibles.put(servidor)

    def generar_llegadas():
        """Genera el proceso de llegadas externas dentro de la ventana configurada."""
        while True:
            intervalo = azar.expovariate(tasa)
            if entorno.now + intervalo >= duracion:
                return
            yield entorno.timeout(intervalo)
            cliente = {
                'cliente_id': len(eventos) + 1,
                'es_preferencial': False,
                'tiempo_entrada_sistema': entorno.now,
                'tiempo_salida_sistema': None,
                'paradas': [],
            }
            eventos.append(cliente)
            entorno.process(atender(cliente))

    entorno.process(generar_llegadas())
    entorno.run()
    nombre_ascii = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode()
    identificador = re.sub(r'[^a-z0-9]+', '_', nombre_ascii.lower()).strip('_') or 'simulacion'
    return {
        'simulacion_id': identificador,
        'duracion_total_minutos': max(duracion, entorno.now),
        'eventos_clientes': eventos,
    }
