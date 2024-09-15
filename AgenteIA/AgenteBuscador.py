from AgenteIA.Agente import Agente
from copy import deepcopy
import time

class AgenteBuscador(Agente):
    def __init__(self, estrategia="A*", heuristica="manhattan"):
        super().__init__()
        self.estrategia = estrategia
        self.heuristica = heuristica
        self.visitados = set()
        self.frontera = []
    
    def programa(self):
        estado_inicial = self.percepciones["estado_inicial"]
        estado_meta = self.percepciones["estado_meta"]
        self.frontera = [(estado_inicial, [])]
        self.visitados = set()
        
        while self.frontera:
            if self.estrategia == "profundidad":
                nodo_actual = self.frontera.pop()
            else:
                nodo_actual = self.frontera.pop(0)
            
            estado_actual, camino_actual = nodo_actual
            
            if estado_actual == estado_meta:
                self.acciones = camino_actual
                return camino_actual
            
            if tuple(estado_actual) not in self.visitados:
                self.visitados.add(tuple(estado_actual))
                sucesores = self.generar_sucesores(estado_actual)
                
                for sucesor in sucesores:
                    nuevo_camino = camino_actual + [sucesor]
                    if self.estrategia in ["A*", "codiciosa"]:
                        self.frontera.append((sucesor, nuevo_camino))
                    else:
                        self.frontera.append((sucesor, nuevo_camino))
            
            if self.estrategia in ["A*", "codiciosa"]:
                self.frontera.sort(key=lambda nodo: self.get_funcion_A(nodo) if self.estrategia == "A*" else self.get_heuristica(nodo))
    
    def generar_sucesores(self, estado):
        sucesores = []
        idx_vacio = estado.index(0)
        movimientos = {
            "arriba": idx_vacio - 3,
            "abajo": idx_vacio + 3,
            "izquierda": idx_vacio - 1,
            "derecha": idx_vacio + 1
        }
        if idx_vacio // 3 > 0:
            sucesores.append(self.mover(estado, idx_vacio, movimientos["arriba"]))
        if idx_vacio // 3 < 2:
            sucesores.append(self.mover(estado, idx_vacio, movimientos["abajo"]))
        if idx_vacio % 3 > 0:
            sucesores.append(self.mover(estado, idx_vacio, movimientos["izquierda"]))
        if idx_vacio % 3 < 2:
            sucesores.append(self.mover(estado, idx_vacio, movimientos["derecha"]))
        return sucesores

    def mover(self, estado, idx_vacio, idx_nuevo):
        nuevo_estado = estado[:]
        nuevo_estado[idx_vacio], nuevo_estado[idx_nuevo] = nuevo_estado[idx_nuevo], nuevo_estado[idx_vacio]
        return nuevo_estado

    def get_funcion_A(self, nodo):
        estado, _ = nodo
        return self.get_costo(estado) + self.get_heuristica(estado)
    
    def get_costo(self, camino):
        return len(camino)

    def get_heuristica(self, estado):
        if self.heuristica == "manhattan":
            return self.heuristica_manhattan(estado)
        elif self.heuristica == "lugar_vacio":
            return self.heuristica_lugar_vacio(estado)
        elif self.heuristica == "combinada":
            return self.heuristica_combinada(estado)
    
    def heuristica_manhattan(self, estado):
        meta = [1, 2, 3, 4, 5, 6, 7, 8, 0]
        return sum(
            abs(fila_actual - fila_meta) + abs(columna_actual - columna_meta)
            for pieza in estado if pieza != 0
            for (fila_actual, columna_actual) in [self.obtener_posicion(pieza, estado)]
            for (fila_meta, columna_meta) in [self.obtener_posicion(pieza, meta)]
        )
    
    def obtener_posicion(self, pieza, estado):
        idx = estado.index(pieza)
        fila = idx // 3
        columna = idx % 3
        return fila, columna

    def buscar_solucion_y_frontera(self, estado_inicial, estado_meta):
        frontera = []
        visitados = set()
        frontera.append((estado_inicial, []))  # (estado, acciones)
        visitados.add(tuple(estado_inicial))
        tamano_frontera_max = 0
        
        while frontera:
            estado_actual, acciones = frontera.pop(0)
            
            if estado_actual == estado_meta:
                return acciones, tamano_frontera_max
            
            for accion, sucesor in self.generar_sucesores_con_accion(estado_actual):
                if tuple(sucesor) not in visitados:
                    visitados.add(tuple(sucesor))
                    frontera.append((sucesor, acciones + [accion]))
                    tamano_frontera_max = max(tamano_frontera_max, len(frontera))
        
        return None, tamano_frontera_max

    def generar_sucesores_con_accion(self, estado):
        sucesores = []
        idx_vacio = estado.index(0)
        
        # Movimientos posibles y las acciones correspondientes
        movimientos = {
            "arriba": idx_vacio - 3,
            "abajo": idx_vacio + 3,
            "izquierda": idx_vacio - 1,
            "derecha": idx_vacio + 1
        }
        acciones = {
            "arriba": 'w',
            "abajo": 's',
            "izquierda": 'a',
            "derecha": 'd'
        }
        
        # Movimiento es válido y si es, generamos el sucesor
        for direccion, nuevo_idx in movimientos.items():
            if (direccion == "arriba" and idx_vacio // 3 > 0) or \
            (direccion == "abajo" and idx_vacio // 3 < 2) or \
            (direccion == "izquierda" and idx_vacio % 3 > 0) or \
            (direccion == "derecha" and idx_vacio % 3 < 2):
                nuevo_estado = self.mover(estado, idx_vacio, nuevo_idx)
                sucesores.append((acciones[direccion], nuevo_estado))
        
        return sucesores
