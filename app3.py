import pygame
import math
import random
import time

# Configuración inicial
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Corazón y Rosas")
clock = pygame.time.Clock()

# Colores
BACKGROUND = (10, 10, 26)
PINK = (255, 20, 147)
LIGHT_PINK = (255, 182, 193)
DARK_PINK = (199, 21, 133)
LEAF_GREEN = (34, 139, 34)
DARK_GREEN = (0, 100, 0)
WHITE = (255, 255, 255)
ROSE_RED = (188, 32, 51)
ROSE_PINK = (255, 105, 180)
ROSE_WHITE = (255, 240, 245)


def ease_out_cubic(x):
    """Función de suavizado cúbica para una animación más natural"""
    return 1 - pow(1 - x, 3)


def dibujar_corazon(surface, x, y, tamaño):
    """Dibuja un corazón completo usando ecuaciones paramétricas"""
    points = []
    for t in range(360):
        theta = math.radians(t)
        px = 16 * math.sin(theta) ** 3
        py = 13 * math.cos(theta) - 5 * math.cos(2*theta) - \
            2 * math.cos(3*theta) - math.cos(4*theta)
        points.append((x + px * tamaño/16, y + py * tamaño/13))

    pygame.draw.polygon(surface, PINK, points)


def dibujar_hoja_rosa(surface, x, y, tamaño, angle):
    """Dibuja una hoja elegante de rosa"""
    points = []
    for t in range(0, 360, 5):
        theta = math.radians(t)
        rx = tamaño * (0.5 + 0.3 * math.cos(2 * theta)) * math.cos(theta/2)
        ry = tamaño * (0.5 + 0.3 * math.sin(2 * theta)) * math.sin(theta/2)

        rotated_x = rx * math.cos(angle) - ry * math.sin(angle)
        rotated_y = rx * math.sin(angle) + ry * math.cos(angle)
        points.append((x + rotated_x, y + rotated_y))

    pygame.draw.polygon(surface, LEAF_GREEN, points)
    pygame.draw.polygon(surface, DARK_GREEN, points, 1)


def dibujar_petalo_rosa(surface, x, y, tamaño, angle, color):
    """Dibuja un pétalo de rosa con curva ajustable"""
    points = []
    for t in range(0, 360, 5):
        theta = math.radians(t)
        rx = tamaño * (0.5 + 0.5 * math.cos(theta)) * math.cos(theta/2)
        ry = tamaño * (0.5 + 0.5 * math.sin(theta)) * math.sin(theta/2)

        rotated_x = rx * math.cos(angle) - ry * math.sin(angle)
        rotated_y = rx * math.sin(angle) + ry * math.cos(angle)
        points.append((x + rotated_x, y + rotated_y))

    pygame.draw.polygon(surface, color, points)


def dibujar_rosa(surface, x, y, escala):
    """Dibuja una rosa con pétalos en espiral"""
    # Tallo
    stem_width = int(4 * escala)
    stem_height = int(200 * escala)
    pygame.draw.line(surface, DARK_GREEN, (x, y),
                     (x, y + stem_height), stem_width)

    # Hojas
    angles = [-0.5, 0.5]
    for angle in angles:
        leaf_x = x + math.cos(angle) * stem_height * 0.3
        leaf_y = y + stem_height * 0.6 + math.sin(angle) * stem_height * 0.3
        dibujar_hoja_rosa(surface, leaf_x, leaf_y, 30 * escala, angle)

    # Pétalos en espiral
    colores_rosa = ['#FF69C4', '#FF1493', '#DC7093']
    tamaño_inicial = 10 * escala

    # Pétalos internos
    for i in range(15):
        angle = math.radians(i * 25)
        dibujar_petalo_rosa(surface, x, y, tamaño_inicial +
                            i * escala, angle, colores_rosa[i % 3])

    # Pétalos externos
    for i in range(15):
        angle = math.radians(i * 25 + 10)
        dibujar_petalo_rosa(surface, x, y, tamaño_inicial +
                            (i + 15) * escala, angle, colores_rosa[(i + 1) % 3])


def escribir_texto_animado(surface, mensaje, y_pos, tamaño, color):
    """Escribe texto con animación elegante"""
    font = pygame.font.Font(None, tamaño)
    text_surface = font.render(mensaje, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH//2, y_pos))
    surface.blit(text_surface, text_rect)


def animacion_principal():
    """Secuencia principal de animación"""
    # Animar corazón creciente
    for i in range(100):
        progress = i / 99
        tamaño_suavizado = ease_out_cubic(progress) * 150
        screen.fill(BACKGROUND)
        dibujar_corazon(screen, WIDTH//2, HEIGHT//3, tamaño_suavizado)
        pygame.display.flip()
        time.sleep(0.02 - (0.015 * progress))

    time.sleep(0.5)

    # Dibujar dos rosas
    for i in range(100):
        progress = i / 99
        screen.fill(BACKGROUND)
        dibujar_corazon(screen, WIDTH//2, HEIGHT//3, 150)
        dibujar_rosa(screen, WIDTH//2 - 150, HEIGHT//2 + 50, 0.8 * progress)
        dibujar_rosa(screen, WIDTH//2 + 150, HEIGHT//2 + 50, 0.8 * progress)
        pygame.display.flip()
        time.sleep(0.02)

    time.sleep(0.5)

    # Añadir texto animado
    for i in range(100):
        progress = i / 99
        screen.fill(BACKGROUND)
        dibujar_corazon(screen, WIDTH//2, HEIGHT//3, 150)
        dibujar_rosa(screen, WIDTH//2 - 150, HEIGHT//2 + 50, 0.8)
        dibujar_rosa(screen, WIDTH//2 + 150, HEIGHT//2 + 50, 0.8)
        escribir_texto_animado(screen, "Feliz", HEIGHT -
                               200, int(36 * progress), PINK)
        escribir_texto_animado(screen, "San Valentin",
                               HEIGHT - 150, int(48 * progress), DARK_PINK)
        pygame.display.flip()
        time.sleep(0.02)

    # Efecto final de brillo
    for _ in range(30):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        pygame.draw.circle(screen, LIGHT_PINK, (x, y), random.randint(2, 5))
        pygame.display.flip()
        time.sleep(0.05)


# Ejecutar animación
animacion_principal()

# Mantener la ventana abierta
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
