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
lista_rezagados: list = []
lista_compra = []


def buscar_dinero(env, datos_estudiante):
    # print('estudiante va a buscar dinero')
    # dinero: int = 15
    lista_rezagados.append(datos_estudiante)


def atender(estudiante, dinero_estudiante, env):
    global duracion
    R = random.random()
    tiempo = TIEMPO_ATENCION_MAX - TIEMPO_ATENCION_MIN
    tiempo_atencion = TIEMPO_ATENCION_MIN + (tiempo * R)
    yield env.timeout(tiempo_atencion)

    comprar_matricula(env, estudiante, dinero_estudiante, tiempo_atencion)
    # print("Tiempo de la atencion para la matricula de %s duró unos %3.1f minutos" % (estudiante[0], tiempo_atencion))
    duracion = duracion + tiempo_atencion


def estudiante_llegada(env, estudiante, dinero_estudiante, personal):
    global tiempo_espera
    global fin
    llega = env.now
    print('\n')
    print("%s llego a la ventanilla en el minuto %2.1f" % (estudiante[0], llega))
    print('con sus datos:')
    print('##################################')
    print('# NOMBRE : ' + estudiante[0])
    print('# CI : ' + estudiante[1])
    print('# COD-SIS : ' + estudiante[2])
    print('##################################')
    with personal.request() as request:
        yield request
        pasa = env.now
        espera = pasa - llega
        tiempo_espera = tiempo_espera + espera
        print(str(estudiante[0]) + " pasa con cajero " + NOMBRE_CAJERO + "en el minuto %3.1f habiendo esperado %2.1f "
                                                                         "minutos" % (
                  pasa, espera))
        yield env.process(atender(estudiante, dinero_estudiante, env))
        deja = env.now
        # print(estudiante[0] + " se direge al rectorado en el minuto %3.1f" % deja)
        # print("<------------------------------------------------------------------->")
        fin = deja


def comprar_matricula(env, datos_estudiante, dinero_estudiante, tiempo_atencion):
    global fin
    reglas_cliente = Estudiante()
    reglas_mesero = Cajero()
    bandera: bool = True
    estudiante = AgenteReactivo(reglas_cliente.reglasEstudiante())
    cajero = AgenteReactivo(reglas_mesero.reglasCajero())
    global estado_cajero
    if estado_cajero:
        if datos_estudiante[0] != '':
            estado_cajero = False
            print("Estudiante " + datos_estudiante[0] + " es atendido por " + NOMBRE_CAJERO + "\n")
            for i in range(1, 6):
                accion_cliente = estudiante.actuar(i, '')
                accion_cajero = cajero.actuar(i + 1, '')

                match accion_cajero:
                    case 'Solicitar':
                        print('   Estudiante ' + datos_estudiante[
                            0] + ' realiza acción ' + accion_cliente + ' matricula \n')
                    case 'Identificarse':
                        print('   Estudiante ' + datos_estudiante[0] + ' realiza acción ' + accion_cliente + '\n')
                        print('   ' + datos_estudiante[0] + ' proporciona sus numero de carnet y codigo sis')
                    case 'Buscar':
                        print('   Cajero ' + NOMBRE_CAJERO + ' realiza acción ' + accion_cajero + '\n')
                        print('   Estudiante ' + datos_estudiante[0] + ' realiza acción ' + accion_cliente + '\n')
                        print('   Cajero ' + NOMBRE_CAJERO + ' encuentra los datos del estudiante ' + datos_estudiante[
                            0] + ' en el sistema \n')
                    case 'Pagar':
                        print('   Estudiante ' + datos_estudiante[0] + ' realiza acción ' + accion_cliente + '\n')
                        print('   Estudiante ' + datos_estudiante[0] + ' paga el monto de Bs ' + str(
                            dinero_estudiante) + '\n')
                        if dinero_estudiante == PRECIO_MATRICULA:
                            print('   Cajero ' + NOMBRE_CAJERO + ' recibe el monto total de Bs' + str(
                                dinero_estudiante) + '\n')
                        elif dinero_estudiante > PRECIO_MATRICULA:
                            print('   Cajero ' + NOMBRE_CAJERO + ' recibe el monto de Bs ' + str(
                                dinero_estudiante) + '\n')
                            print('   Cajero ' + NOMBRE_CAJERO + ' retorna Bs' + str(
                                dinero_estudiante - PRECIO_MATRICULA) + ' de cambio \n')
                        else:
                            print('   el monto no alcanza para pagar la matricula\n')
                            print('   Cajero ' + NOMBRE_CAJERO + ' retorna el monto total de Bs' + str(
                                dinero_estudiante) + '\n')
                            print('   estudiante se retira')
                            res = 'estudiante va a buscar dinero'

                            estado_cajero = True
                            bandera = False

                    case 'Facturar':
                        if bandera:
                            print('   Cajero ' + NOMBRE_CAJERO + ' realiza acción ' + accion_cajero + '\n')
                        # print('   Estudiante ' + nombre + ' realiza acción ' + accion_cliente + '\n')
            # time.sleep(3)
            # print('   Estudiante ' + datos_estudiante[0] + ' obtuvo matricula \n')
            # res = ('---Estudiante ' + datos_estudiante[0] + ' se direge al rectorado--- \n')
            estado_cajero = True
            if bandera:
                print('   Estudiante ' + datos_estudiante[0] + ' obtuvo matricula \n')
                res = ('Estudiante ' + datos_estudiante[0] + ' se direge al rectorado ')
            else:
                res = 'estudiante va a buscar dinero'
                buscar_dinero(env, datos_estudiante)

            deja = env.now

            print("Tiempo de la atencion para la matricula de %s duró unos %3.1f minutos" % (
                datos_estudiante[0], tiempo_atencion))
            print(res + " en el minuto %3.1f" % deja)
            print("<------------------------------------------------------------------->")
            fin = deja
            return res
        else:
            return ''
    else:
        print("Cajero " + NOMBRE_CAJERO + " ocupado\n")
        result = ("---Estudiante " + datos_estudiante[0] + " espera en la cola---\n")
        return result


def generar_estudiante():
    nro_apellidos = [random.randint(0, 102)]
    nro_nombres = [random.randint(0, 454)]
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
    if lista_rezagados:
        lista_compra.remove(lista_rezagados[0][0])
        print('>>>>>>> Estudiante ' + (lista_rezagados[0])[0] + ' vuelve a la fila')
        llegada = obtenr_random()
        yield env.timeout(llegada)
        env.process(estudiante_llegada(env, lista_rezagados[0], 15, personal))
        lista_compra.append(lista_rezagados[0][0])
        lista_rezagados.pop(0)
    else:
        for i in range(0, TOTAL_ESTUDIANTES):
            x = agregar_estudiante()
            estudiante = x.split("-")
            llegada = obtenr_random()
            dinero_estudiante = random.randint(13, 20)
            if estudiante[0] != '':
                lista_compra.append(estudiante[0])
                yield env.timeout(llegada)
                env.process(estudiante_llegada(env, estudiante, dinero_estudiante, personal))

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
    while lista_rezagados:
        env.process(main(env, personal))
        env.run()
    print(lista_compra)
