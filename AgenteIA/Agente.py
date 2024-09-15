# *************************************************************
# * Clase: Agente                                             *
# * Autor: Victor Estevez                                     *
# * Version: v2023.03.29                                      *
# * Descripcion: Implementacion de agente, percibe de su      *
# *              entorno, mapea las percepciones y modifica   *
# *              su entorno para resolucion de problema       *
# *************************************************************


class Agente:
    def __init__(self):
        self.percepciones = None
        self.acciones = []
        self.habilitado = True
        self.mr = None
    
    def percibir(self, percepcion):
        self.percepciones = percepcion
    
    def actuar(self):
        raise NotImplementedError("El método actuar() debe ser implementado por subclases.")
    
    def programa(self):
        raise NotImplementedError("El método programa() debe ser implementado por subclases.")
    
    def reiniciar(self):
        self.percepciones = None
        self.acciones = []
        self.habilitado = True
        self.mr = None
