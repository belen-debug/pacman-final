import random
import pyxel
import time
class Muros:
    def __init__(self, tamano):
        self.tamano = tamano  # Tamaño de los bloques del laberinto
        self.muros = [
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
            [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1],
            [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
            [2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 3, 2],
            [2, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 2],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 1, 0, 1],
            [1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 3, 1, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
        self.puntos = []  # Lista para almacenar las coordenadas de los puntos
        self.pildoras = [] # Lista para almacenar las coordenadas de las píldoras
        self.cereza_x = None  # Coordenada x de la cereza
        self.cereza_y = None  # Coordenada y de la cereza
        self.cereza_visible = False # Indica si la cereza está visible
        # Lista de posiciones válidas para la cereza
        self.posiciones_validas = [(90, 20), (90, 50), (20, 200),(100,20),(90,240)]
        self.tiempo_aparicion_cereza = random.randint(1, 2)  # Entre 10 y 30 segundos
        self.tiempo_desaparicion_cereza = 5  # La cereza estará visible por 5 segundos

        # Generar puntos en las celdas accesibles (celdas con 0)
        for fila in range(len(self.muros)):
            for columna in range(len(self.muros[0])):
                if self.muros[fila][columna] == 0:
                    x = columna * self.tamano + self.tamano // 2
                    y = fila * self.tamano + self.tamano // 2
                    self.puntos.append((x, y))
                if self.muros[fila][columna] == 3:  # Crea las píldoras
                    x = columna * self.tamano + self.tamano // 2
                    y = fila * self.tamano + self.tamano // 2
                    self.pildoras.append((x, y))




    def draw(self):
        """Dibuja el laberinto y los puntos"""
        for row_index, row in enumerate(self.muros):
            for col_index, cell in enumerate(row):
                x = col_index * self.tamano
                y = row_index * self.tamano
                if cell == 1:  # Dibujar muros
                    pyxel.rect(x, y, self.tamano, self.tamano, 1)
                    pyxel.rect(x+2, y+2, 12, 12, 5)

        # Dibujar los puntos restantes
        for (x, y) in self.puntos:
            pyxel.circ(x, y, 2,10)  # Dibujar puntos pequeños
        for (x, y) in self.pildoras:  # Dibujar las píldoras
            pyxel.circ(x, y, 4, 7)
        # Dibuja la cereza
        if self.cereza_visible:
            pyxel.blt(self.cereza_x,self.cereza_y,0,0,89,16,8,0)




