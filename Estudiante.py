class Estudiante():

    def reglasEstudiante(self):
        reglas = {1: 'Solicitar',
                  2: 'Identificarse',
                  3: 'Esperar',
                  4: 'Pagar',
                  5: 'Facturar',
                  6: 'Desplazar',
                  'entregar Orden': 'cliente Satisfecho',
                  'cobrar': 'paga Cuenta y se va '}
        return reglas