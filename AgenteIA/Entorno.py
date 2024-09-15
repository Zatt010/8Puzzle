class Entorno:

    def __init__(self):
        self.__agentes = []
        self.estado_actual = None

    def get_percepciones(self, agente):
        if self.estado_actual is not None:
            agente.percibir(self.estado_actual)
        else:
            print("Estado actual no definido en el entorno.")

    def get_agentes(self):
        return self.__agentes

    def ejecutar(self, agente):
        acciones = agente.acciones
        if acciones:
            ultima_accion = acciones[-1]
            self.estado_actual = ultima_accion
            print(f"Acción ejecutada: {ultima_accion}")

    def evolucionar(self):
        if not self.finalizar():
            for agente in self.__agentes:
                self.get_percepciones(agente)
                self.ejecutar(agente)

    def run(self):
        while True:
            if self.finalizar():
                break
            self.evolucionar()

    def finalizar(self):
        return all(not agente.habilitado for agente in self.__agentes)

    def insertar(self, agente):
        self.__agentes.append(agente)
