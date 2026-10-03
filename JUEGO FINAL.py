#librerias
import sys
import pygame
import random

#iniciar pygame
pygame.init()

#configuracion ventana
ANCHO, ALTO = 800, 600
ventana= pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Cuphead")

#configurar colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (250, 10, 10)
AZUL = (10, 10, 250)
VERDE = (10, 250, 10)
MORADO = (150, 10, 150)

#configurar fuente
fuente = pygame.font.Font(None, 36)
fuente_contador = pygame.font.Font(None, 200)

#cargar sonidos
sonido_explosion = pygame.mixer.Sound("explosion.mp3")
sonido_disparo = pygame.mixer.Sound("disparo.mp3")
sonido_fin = pygame.mixer.Sound("final.mp3")
sonido_gameover = pygame.mixer.Sound("gameover.mp3")
sonido_golpe = pygame.mixer.Sound("golpe.mp3")
sonido_ganar = pygame.mixer.Sound("ganar.mp3")
sonido_inicio = pygame.mixer.Sound("Pantalla.mp3")
sonido_numeros = pygame.mixer.Sound("num.mp3")
sonido_nf = pygame.mixer.Sound("nf.mp3")
pygame.mixer.music.load("Inicio.mp3")
pygame.mixer.music.set_volume(0.7)

#Cargar fondo
fondo = pygame.image.load("fondo.webp")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

#Configurar reloj
reloj = pygame.time.Clock()

#Generar clase jugador
class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.frames_normales = [
            pygame.image.load("j1.png").convert_alpha(),
            pygame.image.load("j2.png").convert_alpha(),
            pygame.image.load("j3.png").convert_alpha(),
            pygame.image.load("j4.png").convert_alpha()
        ]
        self.frames_normales = [pygame.transform.scale(img, (100, 100)) for img in self.frames_normales]

        self.frames_golpe = [
            pygame.image.load("hit1.png").convert_alpha(),
            pygame.image.load("hit2.png").convert_alpha(),
            pygame.image.load("hit3.png").convert_alpha(),
            pygame.image.load("hit4.png").convert_alpha(),
            pygame.image.load("hit5.png").convert_alpha(),
            pygame.image.load("hit6.png").convert_alpha(),
            pygame.image.load("hit7.png").convert_alpha(),
            pygame.image.load("hit8.png").convert_alpha(),
            pygame.image.load("hit9.png").convert_alpha(),
            pygame.image.load("hit10.png").convert_alpha(),
            pygame.image.load("hit11.png").convert_alpha(),
            pygame.image.load("hit12.png").convert_alpha(),
            pygame.image.load("hit13.png").convert_alpha(),
            pygame.image.load("hit14.png").convert_alpha(),
            pygame.image.load("hit15.png").convert_alpha()
        ]
        self.frames_golpe = [pygame.transform.scale(img, (100, 100)) for img in self.frames_golpe]

        self.frames = self.frames_normales
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.vidas = 3

        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100
    
        self.invencible = False
        self.tiempo_invencible = 2000
        self.inicio_invencible = 0

        self.visible = True
    
    def mover(self, keys):
        if keys[pygame.K_DOWN]:
            self.rect.y += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        #Mantener al jugador dentro de los limites de la ventana
        self.rect.clamp_ip(pygame.Rect(0, 0, ANCHO, ALTO))
    
    def herir(self):
        if not self.invencible:
            self.vidas -= 1
            self.invencible = True
            self.inicio_invencible = pygame.time.get_ticks()
            self.index = 0
            sonido_golpe.play()
    
    def update(self):
        now = pygame.time.get_ticks()

        if self.invencible:
            # Invencibilidad y parpadeo
            self.visible = ((now - self.inicio_invencible) % 200) >= 100

            # Animación de golpe
            if now - self.last_update > 120:  # 120  por frame de golpe
                self.last_update = now
                self.index_golpe = (getattr(self, 'index_golpe', 0) + 1) % len(self.frames_golpe)
                self.image = self.frames_golpe[self.index_golpe]

            # Fin de invencibilidad
            if now - self.inicio_invencible > self.tiempo_invencible:
                self.invencible = False
                self.visible = True
                self.index_golpe = 0
        else:
            # Animación normal
            if now - self.last_update > 120:
                self.last_update = now
                self.index = (self.index + 1) % len(self.frames_normales)
                self.image = self.frames_normales[self.index]

#Generación de obstaculo
class Obstaculo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = [
            pygame.image.load("en1.png").convert_alpha(),
            pygame.image.load("en2.png").convert_alpha(),
            pygame.image.load("en3.png").convert_alpha()
        ]
        self.frames = [pygame.transform.scale(img, (90, 110)) for img in self.frames]
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()
        # Posición inicial: al lado derecho de la pantalla
        self.rect.topright = (ANCHO + 50, random.randint(0, ALTO - self.rect.height))
        # Movimiento horizontal
        self.vel_x = random.randint(3, 6)
        # Control de tiempo para animación
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100  # milisegundos entre frames
    
    def update(self):
        #Mover el obstaculo
        self.rect.x -= self.vel_x
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index >= len(self.frames):
                self.index = 0  # Loop continuo
            self.image = self.frames[self.index]
        if self.rect.right < 0:
            self.kill()

#Clase del Disparo
class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("disparo.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 25))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    
    def update(self):
        self.rect.x += 5
        if self.rect.top < 0 :
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = [
            pygame.image.load("x1.png").convert_alpha(),
            pygame.image.load("x2.png").convert_alpha(),
            pygame.image.load("x3.png").convert_alpha(),
            pygame.image.load("x4.png").convert_alpha(),
            pygame.image.load("x5.png").convert_alpha(),
            pygame.image.load("x6.png").convert_alpha(),
            pygame.image.load("x7.png").convert_alpha(),
            pygame.image.load("x8.png").convert_alpha(),
            pygame.image.load("x9.png").convert_alpha(),
            pygame.image.load("x10.png").convert_alpha(),
            pygame.image.load("x11.png").convert_alpha(),
            pygame.image.load("x12.png").convert_alpha(),
            pygame.image.load("x13.png").convert_alpha(),
            pygame.image.load("x14.png").convert_alpha(),
            pygame.image.load("x15.png").convert_alpha(),
            pygame.image.load("x16.png").convert_alpha()
        ]
        self.frames = [pygame.transform.scale(img, (60, 60)) for img in self.frames]
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 100

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.index += 1
            if self.index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.index]


#Instanciar objetos y crear sprites
jugador = Jugador(50, ALTO - 50, AZUL)

#Grupo de obstaculos
obstaculos = pygame.sprite.Group()
disparos = pygame.sprite.Group()
todos_sprites = pygame.sprite.Group(jugador)

#Marcadores
puntuacion = 0 #Numero de enemigos eliminados
tiempo_limite = 65 #Tiempo limite
start_ticks = pygame.time.get_ticks() #Contabilidad el tiempo
puntuacion_ganar = 50 #Puntos a ganar

def reiniciar_juego():
    global jugador, obstaculos, disparos, todos_sprites, puntuacion, start_ticks

    jugador.vidas = 3
    jugador.rect.topleft = (50, ALTO - 50)
    jugador.invencible = False
    jugador.visible = True

    obstaculos.empty()
    disparos.empty()
    todos_sprites.empty()
    todos_sprites.add(jugador)

    puntuacion = 0
    start_ticks = pygame.time.get_ticks()

def pantalla_final_interactiva(imagen_path, sonido_path, puntuacion):
    pygame.mixer.music.stop()  # Detener música de fondo
    canal_fin = sonido_fin.play(-1)

    # Cargar imagen
    img = pygame.image.load(imagen_path).convert_alpha()
    img = pygame.transform.scale(img, (400, 150))
    img_rect = img.get_rect()
    img_rect.centerx = ANCHO // 2
    img_rect.y = -img_rect.height  # empieza arriba

    overlay = pygame.Surface((ANCHO, ALTO))
    overlay.fill((0,0,0))
    overlay_alpha = 0
    velocidad_fade = 5
    velocidad_bajada = 5
    reloj_fade = pygame.time.Clock()

    # Animación de fade + bajada de imagen
    while overlay_alpha < 255 or img_rect.y < ALTO // 3:
        if overlay_alpha < 255:
            overlay_alpha += velocidad_fade
        overlay.set_alpha(min(overlay_alpha,255))
        if img_rect.y < ALTO // 3:
            img_rect.y += velocidad_bajada

        ventana.fill((0,0,0))
        ventana.blit(overlay, (0,0))
        ventana.blit(img, img_rect)
        texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
        ventana.blit(texto_puntuacion, (ANCHO//2 - texto_puntuacion.get_width()//2, img_rect.bottom+20))
        pygame.display.flip()
        reloj_fade.tick(60)

    # Reproducir sonido final
    sonido_extra = pygame.mixer.Sound(sonido_path)
    sonido_extra.play()
    
    # Texto parpadeante
    mostrar_texto = True
    contador_parpadeo = 0
    parpadeo_intervalo = 500

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    # Detener sonido final antes de volver al juego
                    if canal_fin:
                        canal_fin.stop()
                    return  # vuelve al juego

        now = pygame.time.get_ticks()
        if now - contador_parpadeo > parpadeo_intervalo:
            contador_parpadeo = now
            mostrar_texto = not mostrar_texto

        ventana.fill((0,0,0))
        ventana.blit(img, img_rect)
        texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
        ventana.blit(texto_puntuacion, (ANCHO//2 - texto_puntuacion.get_width()//2, img_rect.bottom+20))

        if mostrar_texto:
            texto_enter = fuente.render("Presiona ENTER para volver a jugar", True, BLANCO)
            ventana.blit(texto_enter, (ANCHO//2 - texto_enter.get_width()//2, img_rect.bottom+60))

        pygame.display.flip()
        reloj_fade.tick(60)

def pantalla_inicio():
    canal_inicio = sonido_inicio.play(-1)
    # Cargar fondo distinto
    fondo_inicio = pygame.image.load("fondo inicio.png").convert()
    fondo_inicio = pygame.transform.scale(fondo_inicio, (ANCHO, ALTO))

    # Cargar imagen del título
    titulo_img = pygame.image.load("titulo.png").convert_alpha()
    titulo_img = pygame.transform.scale(titulo_img, (500, 150))
    titulo_rect = titulo_img.get_rect()
    titulo_rect.centerx = ANCHO // 2
    titulo_rect.y = -200  # empieza arriba

    # Texto inferior
    texto_nombre = fuente.render("By: Fatima Galicia", True, NEGRO)
    texto_nombre_rect = texto_nombre.get_rect(center=(ANCHO//2, ALTO - 50))

    # Parpadeo
    mostrar_texto = True
    ultimo_parpadeo = pygame.time.get_ticks()
    intervalo = 500

    # Animación inicial de bajada del título
    running = True
    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if canal_inicio:
                        canal_inicio.stop()  #Detener sonido
                    return  # salir y comenzar el juego

        # Animación del título
        if titulo_rect.y < ALTO//2.5:
            titulo_rect.y += 5

        # Parpadeo del texto
        ahora = pygame.time.get_ticks()
        if ahora - ultimo_parpadeo > intervalo:
            ultimo_parpadeo = ahora
            mostrar_texto = not mostrar_texto

        ventana.blit(fondo_inicio, (0, 0))
        ventana.blit(titulo_img, titulo_rect)
        ventana.blit(texto_nombre, texto_nombre_rect)

        if mostrar_texto:
            texto_enter = fuente.render("Presiona ENTER para iniciar", True, BLANCO)
            ventana.blit(texto_enter, (ANCHO//2 - texto_enter.get_width()//2, ALTO - 120))

        pygame.display.flip()
        reloj.tick(60)

def cuenta_regresiva():
    for i in range(3, 0, -1):
        if i == 3:
            sonido_numeros.play()
        elif i == 2:
            sonido_numeros.play()
        elif i == 1:
            sonido_numeros.play()

        ventana.blit(fondo, (0, 0))

        texto = fuente_contador.render(str(i), True, BLANCO)
        texto_rect = texto.get_rect(center=(ANCHO//2, ALTO//2))
        ventana.blit(texto, texto_rect)

        pygame.display.flip()
        pygame.time.delay(1000)  # 1 segundo por número
    
    sonido_nf.play()
    
    ventana.blit(fondo, (0, 0))

    texto_go = fuente_contador.render("GO!", True, BLANCO)
    texto_go_rect = texto_go.get_rect(center=(ANCHO//2, ALTO//2))
    ventana.blit(texto_go, texto_go_rect)

    pygame.display.flip()
    pygame.time.delay(1000)

#Bucle principal del juego
pantalla_inicio()
cuenta_regresiva()
pygame.mixer.music.play(-1) #Reproducir musica
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #Disparo
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE: #Dispara
                sonido_disparo.play()
                disparo = Disparo(jugador.rect.centerx - 2, jugador.rect.centery)
                disparos.add(disparo)
                todos_sprites.add(disparo)
    #Detectar teclas presionadas
    keys = pygame.key.get_pressed()
    jugador.mover(keys)

    #Generar obstaculos aleatorios
    if random.randint(1, 100) > 98:
        obstaculo = Obstaculo()
        obstaculos.add(obstaculo)
        todos_sprites.add(obstaculo)
    
    #Actualizar Sprites
    todos_sprites.update()
    disparos.update()

    #Detectar colisiones
    colisiones = pygame.sprite.groupcollide(obstaculos, disparos, True, True)
    for obstaculo in colisiones.keys():
        explosion = Explosion(obstaculo.rect.centerx, obstaculo.rect.centery)
        todos_sprites.add(explosion)
        sonido_explosion.play()
        puntuacion += 1

    #Detectar colisiones entre el jugador y obstaculos
    colisiones_jugador = pygame.sprite.spritecollide(jugador, obstaculos, True)
    for obstaculo in colisiones_jugador:
        jugador.herir()

    #Calcular tiempo restante
    tiempo_transcurrido = (pygame.time.get_ticks() - start_ticks) / 1000
    tiempo_restante = max(0, tiempo_limite - tiempo_transcurrido)

    if jugador.vidas <= 0 or (tiempo_restante <= 0 and puntuacion < puntuacion_ganar):
        pantalla_final_interactiva("go.png", "gameover.mp3", puntuacion)
        reiniciar_juego()
        pygame.mixer.music.play(-1)
    
    if puntuacion >= puntuacion_ganar:
        pantalla_final_interactiva("ganar.png", "ganar.mp3", puntuacion)
        reiniciar_juego()
        pygame.mixer.music.play(-1)

    #Dibujar marcador, vidas y tiempo
    texto_puntuacion = fuente.render(f"Puntuación: {puntuacion}", True, BLANCO)
    texto_vidas = fuente.render(f"Vidas: {jugador.vidas}", True, BLANCO)
    texto_tiempo = fuente.render(f"Tiempo: {int(tiempo_restante)} s", True, BLANCO)
    ventana.blit(fondo, (0, 0))
    ventana.blit(texto_puntuacion, (10, 10))
    ventana.blit(texto_vidas, (10, 50))
    ventana.blit(texto_tiempo, (10, 90))

    #Dibujar sprites
    for sprite in todos_sprites:
        if not hasattr(sprite, "visible") or sprite.visible:
            ventana.blit(sprite.image, sprite.rect)

    #Actualizar la antalla
    pygame.display.flip()

    #Controlar la velocidad de fotogramas
    reloj.tick(60)