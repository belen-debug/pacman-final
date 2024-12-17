# FANTASMA"
import pyxel
import random
import math
from pacman1 import Pacman



class Fantasma:
    def __init__(self, x, y, sprite, laberinto, pacman):
        self.x = x  # Posición X
        self.y = y  # Posición Y
        self.sprite = sprite  # Sprite del fantasma (índice para la imagen vertical)
        self.tamano = 8 # Tamaño del fantasma (en píxeles)
        self.laberinto = laberinto  # Referencia al laberinto
        self.direccion = random.choice(['left', 'right', 'up', 'down'])  # Dirección inicial aleatoria
        self.velocidad = 2  # Velocidad de movimiento del fantasma
        self.modo_escape = False
        self.pacman = pacman


    def puede_moverse(self, x, y):
        """Verifica si el fantasma puede moverse a las coordenadas dadas"""
        tamano_celda = self.laberinto.tamano
        matriz = self.laberinto.muros

        # Calcula las celdas ocupadas por el fantasma según su tamaño
        celda_izquierda = int(x // tamano_celda)
        celda_derecha = int((x + self.tamano - 1) // tamano_celda)
        celda_superior = int(y // tamano_celda)
        celda_inferior = int((y + self.tamano - 1) // tamano_celda)

        # Asegurarse de no salir de los límites de la matriz
        if celda_izquierda < 0 or celda_superior < 0 or celda_derecha >= len(matriz[0]) or celda_inferior >= len(
                matriz):
            return False

        # Verifica todas las celdas que ocupa el fantasma
        for fila in range(celda_superior, celda_inferior + 1):
            for columna in range(celda_izquierda, celda_derecha + 1):
                if matriz[fila][columna] == 1:  # Si hay un muro
                    return False

        return True


    def crear_fantasmas():
        # Coordenadas del centro del laberinto (ajustar según tamaño del laberinto)
        centro_x = 120  # Coordenada X en el centro
        centro_y = 120  # Coordenada Y en el centro
        # Lista de fantasmas con diferentes sprites
        fantasmas = [
            Fantasma(centro_x, centro_y, 0, ),  # Primer fantasma (sprite 0)
        ]
        return fantasmas

    def update(self):

        """Actualizar la posición del fantasma con movimiento aleatorio y evitando paredes"""
        nuevo_x, nuevo_y = self.obtener_siguiente_posicion()

        # Verificar si puede moverse a la nueva posición, si no puede, cambiar de dirección aleatoria
        if not self.puede_moverse(nuevo_x, nuevo_y):
            self.direccion = random.choice(['left', 'right', 'up', 'down'])

        # Si puede moverse, actualizamos la posición
        if self.puede_moverse(nuevo_x, nuevo_y):
            self.x, self.y = nuevo_x, nuevo_y
    def obtener_siguiente_posicion(self):
        # Obtiene la siguiente posición, para no repetir el código
        nuevo_x, nuevo_y = self.x, self.y

        # Movimiento según la dirección actual
        if self.direccion == 'left':
            nuevo_x -= self.velocidad
        elif self.direccion == 'right':
            nuevo_x += self.velocidad
        elif self.direccion == 'up':
            nuevo_y -= self.velocidad
        elif self.direccion == 'down':
            nuevo_y += self.velocidad

        return nuevo_x, nuevo_y

    def escapar(self, pacman_x, pacman_y):
        siguiente_x, siguiente_y = self.obtener_siguiente_posicion()
        if not self.puede_moverse(siguiente_x, siguiente_y):

            # Las coordenadas de pacman
            pacman_x, pacman_y = self.pacman.x , self.pacman.y
            # Coordenadas actuales de los fantasmas
            fantasma_x, fantasma_y = self.x , self.y

            movimientos = {"left":None,"right":None,"up":None,"down":None}

            movimientos["left"] = fantasma_x - self.velocidad, fantasma_y
            movimientos["right"] = fantasma_x + self.velocidad, fantasma_y
            movimientos["up"] = fantasma_x, fantasma_y - self.velocidad
            movimientos["down"] = fantasma_x , fantasma_y + self.velocidad

            # Distancia a la cual se encuentra el pacman de un fantasma habiéndose movido una casilla.
            # La casilla a la cual se mueve el fantasma lo vamos a proabar iterando y coger la que la distnacia sea mayor
            distancia_escape = 0

            # Le damos un valor cualquiera por defecto a la direccion de escape
            direccion_escape = "left"

            for direccion,nueva_pos in movimientos.items(): # left, right, down or up
                # POr ejemplo primero con left
                # Calcular con esa direccion y la velocidad que sea la nueva posicion
                # Simulando que se ha movido
                nuevo_fantasma_x , nuevo_fantasma_y = nueva_pos

                if not self.puede_moverse(nuevo_fantasma_x, nuevo_fantasma_y):
                    continue

                distancia = abs(pacman_x - nuevo_fantasma_x) + abs(pacman_y - nuevo_fantasma_y)
                self.x, self.y = nuevo_fantasma_x, nuevo_fantasma_y


                # Voy a usar distancia euclídea aunque hay mejores distancias para este caso.
                # Creo que hay algo llamado distancia de manhattan.
                # Caso sencillo primero y luego se puede afinar el tema de las distancias
                #distancia = math.sqrt((pacman_x - nuevo_fantasma_x) ^ 2 + (pacman_y - nuevo_fantasma_y) ^ 2)

                if distancia > distancia_escape:
                    distancia_escape = distancia
                    direccion_escape = direccion

            # Después del for deberíamos tener la distancia a la que, si el fantasma se muieve en esa direccion
            # debería estar más lejos del pacman

            self.direccion = direccion_escape

        # Mover en la dirección óptima
        if self.direccion == "left":
            self.x -= self.velocidad
        elif self.direccion == "right":
            self.x += self.velocidad
        elif self.direccion == "up":
            self.y -= self.velocidad
        elif self.direccion  == "down":
            self.y += self.velocidad


    def draw(self):
        """Dibuja el fantasma en pantalla usando su sprite (suponiendo que están en una fila vertical)"""

        if self.modo_escape ==  True:
            pyxel.blt(self.x, self.y, 0, 16, 32, self.tamano, self.tamano, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 0, self.sprite *16 , self.tamano, self.tamano, 0)

 



