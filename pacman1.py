# PACMAN
import time
import pyxel



class Pacman:

    def __init__(self, x, y, velocidad, laberinto):
        self.x = x  # Posición inicial en el eje X
        self.y = y  # Posición inicial en el eje Y
        self.velocidad = velocidad  # Velocidad de movimiento (numero de píxeles que se mueve por frame)
        self.laberinto = laberinto  # Referencia al laberinto (muros y puntos)
        self.tamano = 16  # Tamaño del sprite del personaje, para detectar colisiones
        self.direccion = None  # Direccion actual del Pacman
        self.direccion_pendiente = None  # Dirección que el pacman intentará tomar
        self.puntuacion = 0  # Puntuacion acumulada
        self.inicio_pildora = 0
        self.inicio_juego = time.time()
        self.pildora_comida = False
        self.nueva_pildora = False
        self.come_fantasma = False
        pyxel.load("assets/resources/assets.pyxres")  # Carga recursos gráficos para el pacman

    def recoge_punto(self):
        """Verifica si Pacman está en una posición con un punto"""
        puntos_restantes = []  # Lista para almacenar los puntos restantes

        for punto in self.laberinto.puntos:
            px, py = punto  # Coordenadas del punto en el laberinto

            # Calculamos la distancia cuadrada entre el centro de Pacman y el punto
            dx = self.x + self.tamano // 2 - px
            dy = self.y + self.tamano // 2 - py
            distancia_cuadrada = dx ** 2 + dy ** 2

            # Verificar si la distancia es menor que 16 (4 píxeles)
            if distancia_cuadrada <= 16:
                self.puntuacion += 10  # Incrementar la puntuación
            else:
                puntos_restantes.append(punto)  # Si Pacman no recoge el punto, lo mantengo en la lista

        # Actualizamos la lista de puntos con los que no fueron recogidos
        self.laberinto.puntos = puntos_restantes

    def come_pildora(self):

        for pildora in self.laberinto.pildoras:
            px, py = pildora
            centro_x_pacman = self.x + self.tamano // 2
            centro_y_pacman = self.y + self.tamano // 2
            distancia_max = self.tamano // 2 + 4  # La distancia máxima

            # Detectar colisión (distancia entre Pacman y la píldora)
            if abs(centro_x_pacman - px) < distancia_max and abs(centro_y_pacman - py) < distancia_max:
                self.laberinto.pildoras.remove(pildora)  # Eliminar el punto
                self.puntuacion += 50  # Aumentar el puntaje
                # Aquí se debería empezar a ejecutar la funcion de comer fantasmas
                self.pildora_comida = True
                self.nueva_pildora = True
                self.inicio_pildora = time.time()






    def teletransportar(self):
        """ Permite a pacman transportarse de un extremo a otro """
        tamano_celda = self.laberinto.tamano

        # Cuando pacman está en el borde izquierdo del mapa
        if self.x <= 0:
            # Se teletransporta al borde derecho
            # (número de celdas - 1) * tamaño de celda
            self.x = (len(self.laberinto.muros[0]) - 1) * tamano_celda
        # Si Pacman está en el borde derecho (ancho del mapa)
        elif self.x >= (len(self.laberinto.muros[0]) * tamano_celda) - self.tamano:
            # Se teletransporta al borde izquierdo
            self.x = 0

    def puede_moverse(self, x, y):
        """Verifica si el personaje puede moverse a las coordenadas dadas"""
        # Define las celdas y muros del laberinto
        tamano_celda = self.laberinto.tamano
        matriz = self.laberinto.muros

        # Calcula las celdas ocupadas por el personaje
        celda_izquierda = x // tamano_celda
        celda_derecha = (x + self.tamano - 1) // tamano_celda
        celda_superior = y // tamano_celda
        celda_inferior = (y + self.tamano - 1) // tamano_celda

        # Comprueba si encuentra un muro, impediendo el movimiento, si detecta el 2 que señala la celda especial llama a la funcion teletransportar
        for fila in range(celda_superior, celda_inferior + 1):
            for columna in range(celda_izquierda, celda_derecha + 1):
                if matriz[fila][columna] == 1:  # Si hay un muro
                    return False
                elif matriz[fila][columna] == 2:  # Si es un lugar para el teletransporte
                    # Llamo a la función teletransportar
                    self.teletransportar()
                    return True

        # Asegurarse de no salir de los límites de la matriz
        if celda_izquierda < 0 or celda_superior < 0 or celda_derecha >= len(
                matriz[0]) or celda_inferior >= len(
            matriz):
            return False
        # En caso de cumplir los requisitos permite el movimiento
        return True

    def automovimiento(self):
        """ Pacman se mueve automaticamente dependiendo de la dirección asignada por el usuario"""
        # Guarda las coordenadas actuales de pacman en las variables nuevo_x, nuevo_y
        nuevo_x, nuevo_y = self.x, self.y

        # Dependinedo de la direccion que toma pacman, ajusta las coordenadas, controlando la velocidad con self.velocidad
        if self.direccion == 'left':
            nuevo_x -= self.velocidad
        elif self.direccion == 'right':
            nuevo_x += self.velocidad
        elif self.direccion == 'up':
            nuevo_y -= self.velocidad
        elif self.direccion == 'down':
            nuevo_y += self.velocidad

        # Verifica si se puede mover a las nueva posicion seleccionada,actualiza las posiciones
        if self.puede_moverse(nuevo_x, nuevo_y):
            self.x, self.y = nuevo_x, nuevo_y

    def update(self):
        """Actualizar posición y dirección"""
        # Detectar dirección solicitada por el usuario por teclado, y asignar a cada tecla una direccion pendiente
        if pyxel.btn(pyxel.KEY_LEFT):
            self.direccion_pendiente = "left"
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self.direccion_pendiente = "right"
        elif pyxel.btn(pyxel.KEY_UP):
            self.direccion_pendiente = "up"
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.direccion_pendiente = "down"

        # Si Pacman tiene una dirección pendiente, se calcula la nueva posición (X y Y) que correspondería a ese movimiento.
        nuevo_x, nuevo_y = self.x, self.y
        if self.direccion_pendiente == "left":
            nuevo_x -= self.velocidad
        elif self.direccion_pendiente == "right":
            nuevo_x += self.velocidad
        elif self.direccion_pendiente == "up":
            nuevo_y -= self.velocidad
        elif self.direccion_pendiente == "down":
            nuevo_y += self.velocidad

        # Cambiar dirección si es posible, es decir si no colisiona con muro o esta fuera de los límites
        if self.puede_moverse(nuevo_x, nuevo_y):
            self.direccion = self.direccion_pendiente

        # Si la dirección de Pacman ya está establecida, se recalcula la nueva posición en base a la dirección actual (self.direccion)
        nuevo_x, nuevo_y = self.x, self.y
        if self.direccion == "left":
            nuevo_x -= self.velocidad
        elif self.direccion == "right":
            nuevo_x += self.velocidad
        elif self.direccion == "up":
            nuevo_y -= self.velocidad
        elif self.direccion == "down":
            nuevo_y += self.velocidad

        # Se actualizan las posiciones de self.x y self.y
        if self.puede_moverse(nuevo_x, nuevo_y):
            self.x, self.y = nuevo_x, nuevo_y
        # Se llama a la función self.recoge_punto() para verificar si Pacman ha recogido algún punto en la nueva posición
        self.recoge_punto()
        self.come_pildora()




    def draw(self):
        """Dibuja al personaje en pantalla"""
        # Se dibuja el sripe en la pantalla en las coordenadas (self.x, self.y)
        if (pyxel.frame_count//6) % 2:
            pyxel.blt(self.x, self.y, 0, 16, 16, self.tamano, self.tamano, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 16, 0,self.tamano, self.tamano, 0)
        # Se representa en la pantalla la puntuación del jugador
        pyxel.rect(180, 240, 80, 16, 10)
        pyxel.text(184, 244, f"Puntuacion: {self.puntuacion}", 1)
     