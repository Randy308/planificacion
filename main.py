import time
import asyncio
import math

import simpy
import random

from AgenteReactivo import AgenteReactivo
from Cajero import Cajero
from Estudiante import Estudiante

# constantes globales
NOMBRE_CAJERO = 'Sr.Lopez'
SEMILLA = 30
NUM_CAJERO = 1
TIEMPO_ATENCION_MIN = 7
TIEMPO_ATENCION_MAX = 15
T_LLEGADAS = 20
TOTAL_ESTUDIANTES = 5
PRECIO_MATRICULA = 15
# variables globales
estado_cajero = True
contador_cola = 1
tiempo_espera = 0.0
duracion = 0.0
fin = 0.0


def atender(est_nombre, env):
    global duracion
    R = random.random()
    tiempo = TIEMPO_ATENCION_MAX - TIEMPO_ATENCION_MIN
    tiempo_atencion = TIEMPO_ATENCION_MIN + (tiempo * R)
    yield env.timeout(tiempo_atencion)
    comprar_matricula(est_nombre)
    print("Tiempo de la atencion para la matricula de %s duró unos %3.1f minutos" % (est_nombre, tiempo_atencion))

    duracion = duracion + tiempo_atencion


def estudiante_llegada(env, estudiante, personal):
    global tiempo_espera
    global fin
    llega = env.now

    print("%s llego a la ventanilla en minuto %2.1f" % (estudiante[0], llega))
    print('con sus datos:')
    print('##################################')
    print('# NOMBRE : '+estudiante[0])
    print('# CI : ' + estudiante[1])
    print('# COD-SIS : ' + estudiante[2])
    print('##################################')
    with personal.request() as request:
        yield request
        pasa = env.now
        espera = pasa - llega
        tiempo_espera = tiempo_espera + espera
        print(str(estudiante[0]) + " pasa con cajero " + NOMBRE_CAJERO + " en minuto %3.1f habiendo esperado %2.1f" % (
            pasa, espera))

        yield env.process(atender(estudiante[0], env))
        deja = env.now

        print(estudiante[0] + " se direge al rectorado en el minuto %3.1f" % deja)
        print("<------------------------------------------------------------------->")
        fin = deja


def comprar_matricula(nombre):
    reglas_cliente = Estudiante()
    reglas_mesero = Cajero()
    dinero_estudiante = random.randint(13, 20)
    estudiante = AgenteReactivo(reglas_cliente.reglasEstudiante())
    cajero = AgenteReactivo(reglas_mesero.reglasCajero())
    global estado_cajero
    if estado_cajero:

        if nombre != '':
            estado_cajero = False
            # print("Cajero " + NOMBRE_CAJERO + " libre\n")
            print("Estudiante " + nombre + " es atendido por "+NOMBRE_CAJERO+"\n")
            for i in range(1, 6):
                accion_cliente = estudiante.actuar(i, '')
                accion_cajero = cajero.actuar(i+1, '')

                match accion_cajero:
                    case 'Solicitar':
                        print('   Estudiante ' + nombre + ' realiza acción ' + accion_cliente + ' matricula \n')
                    case 'Identificarse':
                        print('   Estudiante ' + nombre + ' realiza acción ' + accion_cliente + '\n')
                        print('   '+nombre+' proporciona sus numero de carnet y codigo sis')
                    case 'Buscar':
                        print('   Cajero ' + NOMBRE_CAJERO + ' realiza acción ' + accion_cajero + '\n')
                        print('   Estudiante ' + nombre + ' realiza acción ' + accion_cliente + '\n')
                        print('   Cajero '+NOMBRE_CAJERO+' encuentra los datos del estudiante '+nombre+'en el sistema\n')
                    case 'Pagar':
                        print('   Estudiante ' + nombre + ' realiza acción ' + accion_cliente + '\n')
                        print('   Estudiante ' + nombre + ' paga el monto de Bs ' + str(dinero_estudiante) + '\n')
                        if dinero_estudiante== PRECIO_MATRICULA:
                            print('   Cajero ' + NOMBRE_CAJERO + ' recibe el monto total de Bs' + str(dinero_estudiante) + '\n')
                        elif dinero_estudiante> PRECIO_MATRICULA:
                            print('   Cajero ' + NOMBRE_CAJERO + ' recibe el monto de Bs ' + str(dinero_estudiante) + '\n')
                            print('   Cajero ' + NOMBRE_CAJERO + ' retorna Bs' + str(dinero_estudiante-PRECIO_MATRICULA) + ' de cambio \n')
                        else:
                            print('   el monto no alcanza para pagar la matricula\n')
                            print('   Cajero ' + NOMBRE_CAJERO + ' retorna el monto total de Bs' + str(dinero_estudiante) + '\n')
                            print('   estudiante se retira')
                            res = 'estudiante se va a casa'
                            estado_cajero = True
                            return res

                    case 'Facturar':
                        print('   Cajero ' + NOMBRE_CAJERO + ' realiza acción ' + accion_cajero + '\n')
                        # print('   Estudiante ' + nombre + ' realiza acción ' + accion_cliente + '\n')
            # time.sleep(3)
            print('   Estudiante ' + nombre + ' obtuvo matricula \n')
            res = ('---Estudiante ' + nombre + ' se direge al rectorado--- \n')
            estado_cajero = True
            return res
        else:
            return ''
    else:
        print("Cajero " + NOMBRE_CAJERO + " ocupado\n")
        result = ("---Estudiante " + nombre + " espera en la cola---\n")
        return result


def generar_estudiante():
    nro_apellidos = [random.randint(1, 103)]
    nro_nombres = [random.randint(1, 455)]
    lista_nombres = open('Conexion/nombres-propios-es.txt', encoding="utf8")
    lista_apellidos = open('Conexion/apellidos-es.txt', encoding="utf8")
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
    with open('cola_espera.txt', 'a+', encoding="utf8") as f:
        global contador_cola
        f.write(str(contador_cola) + '-' + line)
        f.write('\n')
        contador_cola = contador_cola + 1


def obtenr_random():
    R = random.random()
    llegada = -T_LLEGADAS * math.log(R)
    return llegada


def main(env, personal):
    lista_compra = []
    for i in range(0, TOTAL_ESTUDIANTES):
        x = agregar_estudiante()
        estudiante = x.split("-")
        llegada = obtenr_random()

        if estudiante[0] != '':
            # print(">>>>>>>>>>> Estudiante " + estudiante[0] + " llega a la ventanilla\n")
            lista_compra.append(estudiante[0])
            yield env.timeout(llegada)
            env.process(estudiante_llegada(env, estudiante, personal))

        else:
            print('"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""')
            print(estudiante[0])


if __name__ == '__main__':
    # random.seed(random.randint(1,SEMILLA))
    open('cola_espera.txt', 'w').close()
    env = simpy.Environment()
    personal = simpy.Resource(env, NUM_CAJERO)
    env.process(main(env, personal))
    env.run()
