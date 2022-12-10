from AgenteReactivo import AgenteReactivo
from Cajero import Cajero
from Estudiante import Estudiante
import asyncio

import math
import simpy
import random

# constantes globales
NOMBRE_CAJERO = 'Sr.Lopez'
SEMILLA = 30
NUM_CAJERO = 1
TIEMPO_ATENCION_MIN = 15
TIEMPO_ATENCION_MAX = 30
T_LLEGADAS = 20
TIEMPO_SIMULACION = 120
TOTAL_ESTUDIANTES = 5
# variables globlaes
estado_cajero = True
contador_cola = 1
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


async def comprarMatricula(nombre):
    reglas_cliente = Estudiante()
    reglas_mesero = Cajero()
    cliente = AgenteReactivo(reglas_cliente.reglasEstudiante())
    cajero = AgenteReactivo(reglas_mesero.reglasCajero())
    global estado_cajero
    if estado_cajero:

        with open(r'cola_espera.txt', 'r+') as fp:
            primera_linea = fp.readline()
            estudiante = primera_linea.split("-")
            lines = fp.readlines()
            fp.seek(0)
            fp.truncate()
            fp.writelines(lines[1:])
        if estudiante != '':
            estado_cajero = False
            print("Cajero " + NOMBRE_CAJERO + " libre\n")
            print("Estudiante " + estudiante[1] + " es atendido\n")
            for i in range(1, 6):
                accion_cliente = cliente.actuar(i, '')
                print('Estudiante ' + estudiante[1] + ' realiza ' + accion_cliente + '\n')
                accion_cajero = cajero.actuar(accion_cliente, '')
                print('Cajero ' + NOMBRE_CAJERO + ' realiza ' + accion_cliente + '\n')
            await asyncio.sleep(3)
            print('Estudiante ' + estudiante[1] + ' obtuvo matricula \n')
            res = ('Estudiante ' + estudiante[1] + ' se direge al rectorado \n')
            estado_cajero = True
            return res
    else:
        print("Cajero " + NOMBRE_CAJERO + " ocupado\n")
        result = ("Estudiante " + nombre + " espera en la cola\n")
        return result


async def main():
    estudiante = generar_estudiante()
    ci = str(random.randint(1000000, 9999999))
    cod_sis = str(random.randint(201500000, 202299999))
    crear_cola(estudiante + '-' + ci + '-' + cod_sis)
    if estudiante != '':
        print('##################################')
        print(estudiante)
        print('CI : ' + ci)
        print('COD-SIS : ' + cod_sis)
        print('##################################')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            res = asyncio.run(comprarMatricula(estudiante, 'Genaro'))
            print(res)
        except KeyboardInterrupt:
            pass


def generar_estudiante():
    nro_apellidos = [random.randint(1, 103)]
    nro_nombres = [random.randint(1, 455)]
    lista_nombres = open('Conexion/nombres-propios-es.txt')
    lista_apellidos = open('Conexion/apellidos-es.txt')
    result = ''
    for i, line in enumerate(lista_nombres):
        if i in nro_nombres:

            s = ''.join(line.splitlines())
            for j, linez in enumerate(lista_apellidos):
                if j in nro_apellidos:
                    nombre = f'{s} {linez}'
                    result = ''.join(nombre.splitlines())
                    break

    lista_nombres.close()
    lista_apellidos.close()
    return result


def agregar_estudiante():
    estudiante = generar_estudiante()
    ci = str(random.randint(1000000, 9999999))
    cod_sis = str(random.randint(201500000, 202299999))
    result = estudiante + '-' + ci + '-' + cod_sis
    crear_cola(result)
    return result


def crear_cola(line):
    with open('cola_espera.txt', 'a+') as f:
        global contador_cola
        f.write(str(contador_cola) + '-' + line)
        f.write('\n')
        contador_cola = contador_cola + 1


if __name__ == '__main__':
    lista_compra = []

    for i in range(1, 4):
        x = agregar_estudiante()
        estudiante = x.split("-")
        if estudiante[0] != '':
            print(">>>>>>>>>>> Estudiante " + estudiante[0] + " llega a la ventanilla\n")
            lista_compra.append(estudiante[0])
            print('##################################')
            print(estudiante[0])
            print('CI : ' + estudiante[1])
            print('COD-SIS : ' + estudiante[2])
            print('##################################')

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                res = asyncio.run(comprarMatricula(estudiante[0]))
                print(res)
                lista_compra.pop(0)
            except KeyboardInterrupt:
                pass
        else:
            print('"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""')
            print(estudiante[0])

        while lista_compra:

            if estado_cajero:
                if lista_compra:
                    try:
                        res = asyncio.run(comprarMatricula(lista_compra[0]))
                        lista_compra.pop(0)
                        print(res)
                    except KeyboardInterrupt:
                        pass

        if not lista_compra:
            print('no existe cola')
        open('cola_espera.txt', 'w').close()
