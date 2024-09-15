import pygame
import random
from Agente8Puzzle import Agente8Puzzle

# Inicializar Pygame
pygame.init()

# Definir colores, tamaño de la pantalla, etc.
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (255, 0, 0)
VERDE = (0, 255, 0)
ANCHO = 600
ALTO = 500
TAMANIO_CELDA = 100
ESPACIADO = 5 

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("8 Puzzle")

# Función para cargar imágenes
def cargar_imagenes():
    imagenes = {}
    for num in range(1, 9):
        imagen = pygame.image.load(f"imagenes/{num}.png")
        imagen = pygame.transform.scale(imagen, (TAMANIO_CELDA - ESPACIADO, TAMANIO_CELDA - ESPACIADO))
        imagenes[num] = imagen
    return imagenes

imagenes = cargar_imagenes()

# Generar un estado inicial aleatorio resoluble
def es_resoluble(estado):
    inversions = 0
    estado_sin_cero = [num for num in estado if num != 0]
    for i in range(len(estado_sin_cero)):
        for j in range(i + 1, len(estado_sin_cero)):
            if estado_sin_cero[i] > estado_sin_cero[j]:
                inversions += 1
    return inversions % 2 == 0

def generar_estado_inicial():
    estado = list(range(9))  # [0, 1, 2, 3, 4, 5, 6, 7, 8]
    while True:
        random.shuffle(estado)
        if es_resoluble(estado):
            return estado

# Definir el estado inicial y meta
estado_inicial = generar_estado_inicial()
estado_meta = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Crear una instancia del agente de 8 puzzle
agente = Agente8Puzzle(estrategia="codicioso", heuristica="manhattan")

# Variables para contar las acciones
contador_acciones = 0
contador_acciones_ia = 0
juego_terminado = False  # Para verificar si la IA ha resuelto el puzzle

# Función para dibujar el tablero con imágenes
def dibujar_tablero(estado):
    pantalla.fill(BLANCO)
    for i in range(9):
        x = (i % 3) * TAMANIO_CELDA
        y = (i // 3) * TAMANIO_CELDA
        if estado[i] != 0:  # No dibujar el espacio vacío
            pantalla.blit(imagenes[estado[i]], (x + ESPACIADO // 2, y + ESPACIADO // 2))
        pygame.draw.rect(pantalla, BLANCO, [x, y, TAMANIO_CELDA, TAMANIO_CELDA], 1)  # Dibujar borde de las celdas

    if not juego_terminado:  # Si el juego no ha terminado, mostrar el botón de IA
        pygame.draw.rect(pantalla, AZUL, [250, 420, 100, 50])
        fuente_boton = pygame.font.Font(None, 36)
        texto_boton = fuente_boton.render("IAHELP", True, BLANCO)
        pantalla.blit(texto_boton, [270, 430])
    else:  # Si el juego ha terminado, mostrar el botón de volver a jugar
        pygame.draw.rect(pantalla, VERDE, [250, 420, 150, 50])
        fuente_boton = pygame.font.Font(None, 36)
        texto_boton = fuente_boton.render("Volver a jugar", True, BLANCO)
        pantalla.blit(texto_boton, [260, 430])

    # Mostrar contador de acciones del jugador
    fuente_contador = pygame.font.Font(None, 36)
    texto_contador = fuente_contador.render(f"Acciones: {contador_acciones}", True, NEGRO)
    pantalla.blit(texto_contador, [ANCHO - 250, 10])

    # Mostrar contador de acciones de la IA
    texto_contador_ia = fuente_contador.render(f"Acciones IA: {contador_acciones_ia}", True, NEGRO)
    pantalla.blit(texto_contador_ia, [ANCHO - 250, 40])

    pygame.display.flip()

# Función para mover las fichas
def mover_ficha(estado, direccion):
    global contador_acciones
    index_vacio = estado.index(0)
    if direccion == 'a':  # Izquierda
        if index_vacio % 3 != 0:  # No está en la columna de la izquierda
            estado[index_vacio], estado[index_vacio - 1] = estado[index_vacio - 1], estado[index_vacio]
            contador_acciones += 1
    elif direccion == 'd':  # Derecha
        if index_vacio % 3 != 2:  # No está en la columna de la derecha
            estado[index_vacio], estado[index_vacio + 1] = estado[index_vacio + 1], estado[index_vacio]
            contador_acciones += 1
    elif direccion == 'w':  # Arriba
        if index_vacio > 2:  # No está en la fila superior
            estado[index_vacio], estado[index_vacio - 3] = estado[index_vacio - 3], estado[index_vacio]
            contador_acciones += 1
    elif direccion == 's':  # Abajo
        if index_vacio < 6:  # No está en la fila inferior
            estado[index_vacio], estado[index_vacio + 3] = estado[index_vacio + 3], estado[index_vacio]
            contador_acciones += 1
    return estado

# Función para manejar eventos
def manejar_eventos(estado):
    global contador_acciones, contador_acciones_ia, juego_terminado, estado_inicial
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            return False
        if not juego_terminado:  # Solo permitir movimientos o IA si el juego no ha terminado
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:  # Mover izquierda
                    estado = mover_ficha(estado, 'a')
                elif evento.key == pygame.K_d:  # Mover derecha
                    estado = mover_ficha(estado, 'd')
                elif evento.key == pygame.K_w:  # Mover arriba
                    estado = mover_ficha(estado, 'w')
                elif evento.key == pygame.K_s:  # Mover abajo
                    estado = mover_ficha(estado, 's')
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Detectar si se presionó el botón de IAHELP
                x, y = pygame.mouse.get_pos()
                if 250 <= x <= 350 and 420 <= y <= 470:
                    contador_acciones = 0
                    contador_acciones_ia = 0
                    solucion = agente.buscar_solucion(estado, estado_meta)
                    if solucion:
                        print("¡Solución encontrada!")
                        for estado_intermedio in solucion:
                            dibujar_tablero(estado_intermedio)
                            pygame.time.delay(500)  
                            contador_acciones_ia += 1
                        juego_terminado = True
                        pygame.time.delay(3000)  
                    else:
                        print("No se encontró solución.")
        else:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Detectar si se presionó el botón de "Volver a jugar"
                x, y = pygame.mouse.get_pos()
                if 250 <= x <= 400 and 420 <= y <= 470:
                    estado_inicial = generar_estado_inicial()
                    estado[:] = estado_inicial[:]  # Reiniciar el estado
                    juego_terminado = False  # Reiniciar el estado del juego
                    contador_acciones = 0
                    contador_acciones_ia = 0
    return True

# Bucle principal del juego
def ejecutar_juego():
    estado_actual = estado_inicial.copy()
    global contador_acciones
    corriendo = True
    while corriendo:
        dibujar_tablero(estado_actual)
        corriendo = manejar_eventos(estado_actual)

    pygame.quit()
