import time
import random
from Agente8Puzzle import Agente8Puzzle

def generar_estado_inicial():
    estado = list(range(9))  # [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while True:
        random.shuffle(estado)
        if es_resoluble(estado):
            return estado

def es_resoluble(estado):
    inversions = 0
    estado_sin_cero = [num for num in estado if num != 0]
    for i in range(len(estado_sin_cero)):
        for j in range(i + 1, len(estado_sin_cero)):
            if estado_sin_cero[i] > estado_sin_cero[j]:
                inversions += 1
    return inversions % 2 == 0

def evaluar_busqueda(agente, estado_inicial, estado_meta):
    start_time = time.time()
    print(f"Evaluando estado inicial: {estado_inicial}")
    solucion, tamano_frontera = agente.buscar_solucion_y_frontera(estado_inicial, estado_meta)
    end_time = time.time()
    
    tiempo = end_time - start_time
    print(f"Tiempo de resolución: {tiempo:.2f} segundos")
    
    optima = len(solucion) if solucion else float('inf')
    
    return solucion, optima, tiempo, tamano_frontera

def main():
    heuristicas = ["manhattan", "lugar_vacio", "combinada"]
    estrategias = ["codicioso", "A*"]
    
    num_problemas = 1000
    
    for heuristica in heuristicas:
        for estrategia in estrategias:
            agente = Agente8Puzzle(estrategia=estrategia, heuristica=heuristica)
            print(f"Evaluando estrategia {estrategia} con heurística {heuristica}...")
            
            soluciones = []
            tiempos = []
            tamanos_frontera = []
            soluciones_encontradas = 0
            
            for i in range(num_problemas):
                print(f"Problema {i + 1}/{num_problemas}")
                estado_inicial = generar_estado_inicial()
                estado_meta = [1, 2, 3, 4, 5, 6, 7, 8, 0]
                
                solucion, optima, tiempo, tamano_frontera = evaluar_busqueda(agente, estado_inicial, estado_meta)
                
                if solucion is not None:
                    soluciones_encontradas += 1
                    soluciones.append(len(solucion))
                    tiempos.append(tiempo)
                    tamanos_frontera.append(tamano_frontera)
            
            probabilidad_exito = soluciones_encontradas / num_problemas
            promedio_tiempo = sum(tiempos) / len(tiempos) if tiempos else float('inf')
            max_tamano_frontera = max(tamanos_frontera) if tamanos_frontera else 0
            
            print(f"Heurística {heuristica}, Estrategia {estrategia}:")
            print(f"Probabilidad de éxito: {probabilidad_exito:.2f}")
            print(f"Tiempo promedio de resolución: {promedio_tiempo:.2f} segundos")
            print(f"Tamaño máximo de la frontera: {max_tamano_frontera}")
            print(f"¿Siempre se encontraron soluciones? {'Sí' if soluciones_encontradas == num_problemas else 'No'}")
            print()

if __name__ == "__main__":
    main()
