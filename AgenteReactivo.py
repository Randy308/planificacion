class AgenteReactivo():
    def __init__(self, reglas):
        self.reglas = reglas

    def actuar(self, percepcion):
        if percepcion in self.reglas.keys():
            return self.reglas[percepcion]
        else:
            return ''
