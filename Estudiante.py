import random


class Estudiante():

    def reglas_estudiante(self,compra_matricula=True):
        if compra_matricula:
            reglas = {1: 'Solicitar',
                      2: 'Identificarse',
                      3: 'Esperar',
                      4: 'Pagar',
                      5: 'Facturar',
                      6: 'Desplazar'
                      }
        else:
            reglas = {1: 'Solicitar',
                      2: 'Dictar',
                      3: 'Elegir',
                      4: 'Esperar',
                      5: 'Devolver',
                      6: 'Retirarse'
                      }
        return reglas


