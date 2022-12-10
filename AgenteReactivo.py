class AgenteReactivo():
    def __init__(self, reglas):
        self.reglas = reglas

    def actuar(self, percepcion, accionBasica=''):
        if not percepcion:
            return accionBasica
        if percepcion in self.reglas.keys():
            return self.reglas[percepcion]
        return accionBasica
