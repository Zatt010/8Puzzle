from AgenteIA.AgenteBuscador import AgenteBuscador
class Agente8Puzzle(AgenteBuscador):
    def __init__(self, estrategia="A*", heuristica="manhattan"):
        super().__init__(estrategia, heuristica)
    
    def buscar_solucion(self, estado_inicial, estado_meta):
        percepcion = {
            "estado_inicial": estado_inicial,
            "estado_meta": estado_meta
        }
        self.percibir(percepcion)
        return self.programa()

    def buscar_solucion(self, estado_inicial, estado_meta):
        percepcion = {
            "estado_inicial": estado_inicial,
            "estado_meta": estado_meta
        }
        self.percibir(percepcion)
        return self.programa()
