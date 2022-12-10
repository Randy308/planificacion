import math
import simpy
import random

estado_cajero = True
contador_cola = 1
NOMBRE_CAJERO = 'Sr.Lopez'
SEMILLA = 30
NUM_CAJERO = 1
TIEMPO_ATENCION_MIN = 15
TIEMPO_ATENCION_MAX = 30
T_LLEGADAS = 20
TIEMPO_SIMULACION = 120
TOTAL_ESTUDIANTES = 5
tiempo_espera = 0.0
duracion = 0.0
fin = 0.0


def atender(cliente, env):
    global duracion
    R = random.random()
    tiempo = TIEMPO_ATENCION_MAX - TIEMPO_ATENCION_MIN
    tiempo_atencion = TIEMPO_ATENCION_MIN + (tiempo * R)
    yield env.timeout(tiempo_atencion)
    print("Matricula entregada a %s en %3.1f minutos" % (cliente, tiempo_atencion))
    duracion = duracion + tiempo_atencion


def cliente(env, name, personal):
    global tiempo_espera
    global fin
    llega = env.now
    print("%s llego a la ventanilla en minuto %2.1f" % (name, llega))
    with personal.request() as request:
        yield request
        pasa = env.now
        espera = pasa - llega
        tiempo_espera = tiempo_espera + espera
        print(str(name) + " pasa con cajero " + NOMBRE_CAJERO + " en minuto %3.1f habiendo esperado %2.1f" % (
            pasa, espera))
        yield env.process(atender(name, env))
        deja = env.now
        print(name + " deja peluqueria en el minuto %3.1f" % deja)
        fin = deja


def principal(env, personal):
    for i in range(TOTAL_ESTUDIANTES):
        R = random.random()
        llegada = -T_LLEGADAS * math.log(R)
        yield env.timeout(llegada)
        i += 1
        env.process(cliente(env, 'Estudiante %d' % i, personal))


random.seed(SEMILLA)
env = simpy.Environment()  # Crea el objeto entorno de simulacion
personal = simpy.Resource(env, NUM_CAJERO)  # Crea los recursos (peluqueros)
env.process(principal(env, personal))  # Invoca el proceso princial
env.run()
