import math
import simpy
import random
import materias
from AgenteReactivo import AgenteReactivo
from Cajero import Cajero
from Estudiante import Estudiante
from Director import Director
from Encargado import Encargado

# constantes globales
NOMBRE_CAJERO = 'Sr.Lopez'
NOMBRE_ENCARGADO = 'Sra .Aguilar'
NOMBRE_DIRECTOR = 'Lic. YONY RICHARD MONTOYA BURGOS'
SEMILLA = 30
NUM_CAJERO = 1
NUM_JEFE_RECTORADO = 1
TIEMPO_ATENCION_MIN = 7
TIEMPO_ATENCION_MAX = 15
T_LLEGADAS = 20
SEMESTRE = '2-2022'
TOTAL_ESTUDIANTES = 5
PRECIO_MATRICULA = 14
PROMEDIO_ATENCION_RECTORADO = 11
LIMITE_MATERIAS_INCRIPCION = 6
# variables globales
estado_cajero = True
estado_rectorado = True
contador_cola = 1
tiempo_espera = 0.0
duracion = 0.0
fin = 0.0
lista_rezagados: list = []
lista_compra = []
tiempo_espera_rectorado = 0.0


def atencion_rectorado(env, estudiante, nivel_estudiante):
    global duracion

    tiempo = TIEMPO_ATENCION_MAX - TIEMPO_ATENCION_MIN
    tiempo_atencion_rec = TIEMPO_ATENCION_MIN + (tiempo * random.random())
    yield env.timeout(tiempo_atencion_rec)

    inscribirse(env, estudiante, tiempo_atencion_rec, materias.obtener_materias_nivel(nivel_estudiante))
    duracion = duracion + tiempo_atencion_rec


def estudiante_llegada_rectorado(env1, estudiante, personal, llega):
    global tiempo_espera_rectorado
    llega = env1.now
    nivel = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    nivel_estudiante = random.choice(nivel)
    print('\n')
    print("%s llego al rectorado en el minuto %2.1f" % (estudiante[0], llega))
    print('con sus matricula adquirida:')
    print('##################################')
    print('# NOMBRE : ' + estudiante[0])
    print('# NIVEL DE ESTUDIOS : ' + nivel_estudiante)
    print('##################################')
    with personal.request() as request:
        yield request
        pasa = env1.now
        espera = pasa - llega
        tiempo_espera_rectorado = tiempo_espera_rectorado + espera
        print(str(estudiante[
                      0]) + " pasa con el Director de carrera " + NOMBRE_DIRECTOR + " en el minuto %3.1f habiendo "
                                                                                    "esperado %2.1f minutos" % (pasa,
                                                                                                                espera))

        yield env1.process(atencion_rectorado(env1, estudiante, nivel_estudiante))


def buscar_dinero(env, datos_estudiante):
    lista_rezagados.append(datos_estudiante)


def atender(estudiante, dinero_estudiante, env):
    global duracion
    R = random.random()
    tiempo = TIEMPO_ATENCION_MAX - TIEMPO_ATENCION_MIN
    tiempo_atencion = TIEMPO_ATENCION_MIN + (tiempo * R)
    yield env.timeout(tiempo_atencion)
    comprar_matricula(env, estudiante, dinero_estudiante, tiempo_atencion)
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
        fin = deja


def inscribirse(env, datos_estudiante, tiempo_atencion, materias_nivel):
    reglas_estudiante = Estudiante()
    reglas_encargado = Encargado()
    reglas_director = Director()
    estudiante = AgenteReactivo(reglas_estudiante.reglas_estudiante(False))
    director = AgenteReactivo(reglas_director.reglas_director())
    encargado = AgenteReactivo(reglas_encargado.reglas_encargado())
    global estado_rectorado
    if estado_rectorado:
        if datos_estudiante[0] != '':
            estado_rectorado = False
            print('<---------------------------------------------------------------------------------------->')
            print("Estudiante " + datos_estudiante[0] + " es atendido por " + NOMBRE_DIRECTOR + "\n")
            for i in range(1, 7):
                accion_estudiante = estudiante.actuar(i)
                accion_director = director.actuar(i)
                match accion_estudiante:

                    case 'Solicitar':

                        print('   Estudiante ' + datos_estudiante[0] +
                              ' realiza acción ' + accion_estudiante + ' inscripción \n')
                    case 'Dictar':
                        print('   Estudiante ' + datos_estudiante[0] +
                              ' realiza acción ' + accion_estudiante + ' las materias habilitadas para esta gestión \n')
                        print('   Director ' + NOMBRE_DIRECTOR +
                              ' menciona las materias habilitadas para este semestre de ' + SEMESTRE + ', las cuales '
                                                                                                       'son:\n')
                        for materias_men in materias_nivel:
                            print('    ' + materias_men[0])
                    case 'Elegir':
                        if len(materias_nivel) > LIMITE_MATERIAS_INCRIPCION:

                            print('   Estudiante ' + datos_estudiante[0] +
                                  ' realiza acción de ' + accion_estudiante + ' grupos solamente para 6 materias '
                                                                              'como limite\n')
                        else:
                            print('   Estudiante ' + datos_estudiante[0] +
                                  ' realiza acción de ' + accion_estudiante + ' los grupos de todas las  materias '
                                                                              'disponibles\n')
                        random.shuffle(materias_nivel)
                        i = 0
                        for materia in materias_nivel:
                            if i < LIMITE_MATERIAS_INCRIPCION:
                                mat = materia[3]
                                mat_aleatoria = random.choice(mat)
                                print('    Estudiante escoge la materia %s con el grupo %d de Lic. %s' % (
                                    materia[0], mat.index(mat_aleatoria) + 1, mat_aleatoria.title()))

                            else:
                                break
                            i += 1
                        print('')
                    case 'Esperar':
                        print('   Estudiante ' + datos_estudiante[0] +
                              ' realiza acción de ' + accion_estudiante + ' transacción \n')
                        for j in range(4):

                            accion_encargado = encargado.actuar(j)

                            match accion_encargado:
                                case 'Entregar':
                                    accion_director = director.actuar(4 + j)
                                    print('     Director ' + NOMBRE_DIRECTOR +
                                          ' realiza acción ' + accion_director + ' documentos de inscripcion del '
                                                                                 'estudiante \n')
                                    print('     Encargado ' + NOMBRE_ENCARGADO +
                                          ' recibe los documentos para la inscripcion del estudiante \n')
                                case 'Habilitar':
                                    print('     Encargado ' + NOMBRE_ENCARGADO +
                                          ' realiza acción de ' + accion_encargado + ' las materias del estudiante \n')
                                case 'Confirmar':
                                    accion_director = director.actuar(3 + j)
                                    print('     Encargado ' + NOMBRE_ENCARGADO +
                                          ' realiza acción ' + accion_encargado + ' al director ' + NOMBRE_DIRECTOR +
                                          ' sobre la incripcion del estudiante \n')

                    case 'Devolver':
                        print('   Director ' + NOMBRE_DIRECTOR +
                              ' realiza acción ' + accion_director + ' la matricula del estudiante \n')
                        print('   Estudiante ' + datos_estudiante[0] +
                              ' recibe devuelta su  matricula \n')
                    case 'Retirarse':

                        print('   Estudiante ' + datos_estudiante[0] +
                              ' realiza acción de ' + accion_estudiante)
                        print('Proceso de inscripcion completada en el minuto %2.1f' % tiempo_atencion)

            print('<---------------------------------------------------------------------------------------->')
            estado_rectorado = True
    else:
        print("Director " + NOMBRE_DIRECTOR + " ocupado\n")
        result = ("Estudiante " + datos_estudiante[0] + " espera en la cola\n")
        return result


def comprar_matricula(env, datos_estudiante, dinero_estudiante, tiempo_atencion):
    global fin
    reglas_estudiante = Estudiante()
    reglas_mesero = Cajero()
    bandera: bool = True
    estudiante = AgenteReactivo(reglas_estudiante.reglas_estudiante())
    cajero = AgenteReactivo(reglas_mesero.reglasCajero())
    global estado_cajero
    if estado_cajero:
        if datos_estudiante[0] != '':
            estado_cajero = False
            print("Estudiante " + datos_estudiante[0] + " es atendido por " + NOMBRE_CAJERO + "\n")
            for i in range(1, 6):
                accion_estudiante = estudiante.actuar(i)
                accion_cajero = cajero.actuar(i)

                match accion_cajero:
                    case 'Solicitar':
                        print('   Estudiante ' + datos_estudiante[
                            0] + ' realiza acción ' + accion_estudiante + ' matricula \n')
                    case 'Identificarse':
                        print('   Estudiante ' + datos_estudiante[0] + ' realiza acción ' + accion_estudiante + '\n')
                        print('   ' + datos_estudiante[0] + ' proporciona sus numero de carnet y codigo sis')
                    case 'Buscar':
                        print('   Cajero ' + NOMBRE_CAJERO + ' realiza acción ' + accion_cajero + '\n')
                        print('   Estudiante ' + datos_estudiante[0] + ' realiza acción ' + accion_estudiante + '\n')
                        print('   Cajero ' + NOMBRE_CAJERO + ' encuentra los datos del estudiante ' + datos_estudiante[
                            0] + ' en el sistema \n')
                    case 'Pagar':
                        print('   Estudiante ' + datos_estudiante[0] + ' realiza acción ' + accion_estudiante + '\n')
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
                            print('   Cajero ' + NOMBRE_CAJERO + ' no recibe el monto total de Bs' + str(
                                dinero_estudiante) + '\n')
                            print('   estudiante se retira')

                            estado_cajero = True
                            bandera = False

                    case 'Facturar':
                        if bandera:
                            print('   Cajero ' + NOMBRE_CAJERO + ' realiza acción ' + accion_cajero + '\n')

            ultima_accion = estudiante.actuar(6)
            estado_cajero = True
            deja_cajero = env.now
            if bandera:
                print('   Estudiante ' + datos_estudiante[0] + ' obtuvo matricula \n')
                res = ('Estudiante ' + datos_estudiante[0] + ' realiza la accion ' + ultima_accion + ', se direge al '
                                                                                                     'rectorado ')

                datos_estudiante.append(str(deja_cajero))
                crear_cola('-'.join(datos_estudiante))
                lista_compra.append(datos_estudiante)
            else:
                res = ('Estudiante ' + datos_estudiante[0] + ' realiza la accion ' + ultima_accion + ', estudiante va '
                                                                                                     'a buscar dinero'
                                                                                                     ' ')
                # res = 'estudiante va a buscar dinero'
                buscar_dinero(env, datos_estudiante)

            print("Tiempo de la atencion para la matricula de %s duró unos %3.1f minutos" % (
                datos_estudiante[0], tiempo_atencion))
            print(res + " en el minuto %3.1f" % deja_cajero)
            print("<------------------------------------------------------------------->")
            fin = deja_cajero
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
        print('>>>>>>> Estudiante ' + (lista_rezagados[0])[0] + ' vuelve a la fila')
        llegada = obtenr_random()
        yield env.timeout(llegada)
        env.process(estudiante_llegada(env, lista_rezagados[0], PRECIO_MATRICULA, personal))
        lista_rezagados.pop(0)
    else:
        if estado_cajero:
            for i in range(0, TOTAL_ESTUDIANTES):
                x = agregar_estudiante()
                estudiante = x.split("-")
                llegada = obtenr_random()
                dinero_estudiante = random.randint(12, 20)
                if estudiante[0] != '':
                    yield env.timeout(llegada)
                    env.process(estudiante_llegada(env, estudiante, dinero_estudiante, personal))
                else:
                    print('"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""')
                    print(estudiante[0])
        else:
            random.shuffle(lista_compra)
            for est in lista_compra:
                llega = obtenr_random()
                yield env.timeout(llega)
                env.process(estudiante_llegada_rectorado(env, est, personal, llega))


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

    estado_cajero = False
    if not lista_rezagados:
        print('''\
              _____  _             _        _                     _            _             
             |  __ \(_)           | |      (_)                   (_)          (_)            
             | |  | |_  __ _    __| | ___   _ _ __  ___  ___ _ __ _ _ __   ___ _  ___  _ __  
             | |  | | |/ _` |  / _` |/ _ \ | | '_ \/ __|/ __| '__| | '_ \ / __| |/ _ \| '_ \ 
             | |__| | | (_| | | (_| |  __/ | | | | \__ \ (__| |  | | |_) | (__| | (_) | | | |
             |_____/|_|\__,_|  \__,_|\___| |_|_| |_|___/\___|_|  |_| .__/ \___|_|\___/|_| |_|
                                                                   | |                       
                                                                   |_|                       
        ''')
        env1 = simpy.Environment()
        rectorado = simpy.Resource(env1, NUM_JEFE_RECTORADO)
        env1.process(main(env1, rectorado))
        env1.run()
