import pygame
import random
import math
import io
from pygame import mixer

# inicializar a pygame
pygame.init()

# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo e icono
pygame.display.set_caption("Galaga")
icono = pygame.image.load("cohete-espacial.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load("Fondo.jpg")

# Variables del Jugador
img_jugador = pygame.image.load("astronave.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# Agregar musica
mixer.music.load("MusicaFondo.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)  # -1 para repetir cada vez que termine

# Variables del Enemigo
# Se crean listas para poder generar mas de 1 enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 10

for e in range(cantidad_enemigos):
    # Dentro de las listas se guardan las variables del enemigo mediante el metodo append
    # proporcional a la cantidad determinada de enemigos en cantidad enemigos
    img_enemigo.append(pygame.image.load("ciencia-ficcion.png"))
    enemigo_x.append(random.randint(0, 736))  # De esta manera el enemigo aparecera en puntos aleatorios
    enemigo_y.append(random.randint(50, 200))  # tomando en cuenta su valor de 64px
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# Variables de la bala
# Se crea una lista para almacenar las balas disparadas
balas = []
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 2
bala_visible = False

# Puntaje
puntaje = 0
fuente = pygame.font.Font('freesansbold.ttf', 32)
texto_x = 10
texto_y = 10

# Texto al final de juego
fuente_final = pygame.font.Font('freesansbold.ttf', 40)


def fuente_bytes(fuente_):
    # Abre el archivo TTF en modo lectura binaria
    with open(fuente_, 'rb') as f:
        # Lee todos los bytes del archivo y los almacena en una variable
        ttf_bytes = f.read()
    # Crea un objeto BytesIO a partir de los bytes del archivo TTF
    return io.BytesIO(ttf_bytes)


fuente_como_bytes = fuente_bytes("FreeSansBold.ttf")
fuente_final_ = pygame.font.Font(fuente_como_bytes, 40)


def texto_final():
    mi_fuente_final = fuente_final_.render("JUEGO TERMINADO", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final, (50, 250))


# Funcion mostrar puntaje
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))


# Funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))


# Funcion Enemigo
def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))


# Funcion disparar bala
def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))


# Funcion detectar colisiones
def hay_colision(x_1, y_1, x_2, y_2):
    # Recuerda la formula de colisiones D=raizcuadrada((x1-x2)alcuadrado + (y2-y1)alcuadrado)
    distancia = math.sqrt(math.pow(x_1 - x_2, 2) + math.pow(y_2 - y_1, 2))
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego
se_ejecuta = True
while se_ejecuta:
    # Imagen de fondo
    pantalla.blit(fondo, (0, 0))

    # Iterar eventos
    for evento in pygame.event.get():

        # Evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1

            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1

            if evento.key == pygame.K_SPACE:
                # En vez de actualizar la posicion de la bala, crea una nueva con su propia
                # posicion y velocidad, esta se agrega a la lista de balas
                sonido_bala = mixer.Sound("disparo.mp3")
                sonido_bala.play()
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -5
                }
                balas.append(nueva_bala)
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        # Evento soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar ubicacion del jugador
    jugador_x += jugador_x_cambio

    # Mantener dentro de bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736  # Esto debido a que el marco es de 800px y la nave es de 64px

    # Modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):

        # Fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]
        # La [e] es el indice que le pertenece al enemigo segun la iteracion donde se encuentre
        # Mantener dentro de bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.9
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.9  # Esto debido a que el marco es de 800px y la nave es de 64px
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colision
        # Se itera y verifica la posicion de cada bala para cada enemigo
        for bala in balas:
            colision_bala_enemigo = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision_bala_enemigo:
                sonido_colision = mixer.Sound("Golpe.mp3")
                sonido_colision.set_volume(0.3)
                sonido_colision.play()
                balas.remove(bala)
                puntaje += 1
                enemigo_x[e] = random.randint(0, 736)  # De esta manera el enemigo aparecera en puntos aleatorios
                enemigo_y[e] = random.randint(50, 200)  # tomando en cuenta su valor de 64px
                break
        """colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            
            bala_y = 500
            bala_visible = False
            """

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento bala
    for bala in balas:
        # Para cada bala en la lista de balas, se actualiza su posicion en el eje Y y dibuja la
        # imagen de la bala en la pantalla
        # Si la bala sale de la pantalla (es decir, si su posicion en el eje Y es menor que cero)
        # elimina esa bala de la lista de balas
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)
    """if bala_y <= -24:
        bala_y = 500
        bala_visible = False"""

    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)

    # Actualizar
    pygame.display.update()
