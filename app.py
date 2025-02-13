import pygame
import sys
import math
import random
from pygame import gfxdraw
import time

# Inicialización
pygame.init()
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animación de Amor")
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


def draw_heart(surface, x, y, size, color):
    """Dibuja un corazón con antialiasing"""
    points = []
    for t in range(360):
        theta = math.radians(t)
        px = 16 * math.sin(theta) ** 3
        py = -(13 * math.cos(theta) - 5 * math.cos(2*theta) -
               2 * math.cos(3*theta) - math.cos(4*theta))
        points.append((int(x + px * size/16), int(y + py * size/16)))

    pygame.gfxdraw.filled_polygon(surface, points, color)
    pygame.gfxdraw.aapolygon(surface, points, color)


def draw_realistic_petal(surface, x, y, size, angle, color, layer, progress):
    """Dibuja un pétalo realista con animación gradual"""
    points = []
    max_size = size * progress

    for t in range(0, 360, 5):
        theta = math.radians(t)
        rx = max_size * (0.5 + 0.5 * math.cos(theta)) * math.cos(theta/2)
        ry = max_size * (0.5 + 0.5 * math.sin(theta)) * math.sin(theta/2)

        variation = 0.1 * math.sin(3 * theta) * layer
        rx += variation
        ry += variation

        rotated_x = rx * math.cos(angle) - ry * math.sin(angle)
        rotated_y = rx * math.sin(angle) + ry * math.cos(angle)
        points.append((int(x + rotated_x), int(y + rotated_y)))

    base_color = pygame.Color(color)
    shadow_color = base_color.lerp((0, 0, 0), 0.2)
    highlight_color = base_color.lerp((255, 255, 255), 0.1)

    pygame.draw.polygon(surface, base_color, points)
    pygame.draw.polygon(surface, shadow_color, points, 1)

    for i in range(int(10 * progress)):
        tx = random.randint(int(x - max_size/2), int(x + max_size/2))
        ty = random.randint(int(y - max_size/2), int(y + max_size/2))
        if pygame.Rect(x - max_size/2, y - max_size/2, max_size, max_size).collidepoint(tx, ty):
            pygame.draw.circle(surface, highlight_color, (tx, ty), 1)


def draw_realistic_rose(surface, x, y, size, color, progress):
    """Dibuja una rosa realista con animación gradual"""
    # Tallo (aparece primero)
    stem_width = size // 10
    stem_height = size * 1.5
    if progress > 0.2:
        current_stem_height = min(
            stem_height, stem_height * (progress - 0.2) * 5)
        pygame.draw.line(surface, DARK_GREEN, (x, y),
                         (x, y + current_stem_height), stem_width)

    # Hojas (aparecen después del tallo)
    if progress > 0.4:
        num_leaves = 2
        for i in range(num_leaves):
            leaf_progress = min(1, (progress - 0.4) * 2)
            leaf_size = size * 0.6 * leaf_progress
            leaf_angle = math.radians(45 + i * 90)
            leaf_x = x + math.cos(leaf_angle) * size * 0.3
            leaf_y = y + stem_height * 0.6 + math.sin(leaf_angle) * size * 0.3
            draw_realistic_leaf(surface, leaf_x, leaf_y,
                                leaf_size, leaf_angle, leaf_progress)

    # Capas de pétalos (aparecen gradualmente)
    if progress > 0.6:
        num_layers = 5
        petal_counts = [5, 8, 12, 16, 20]
        size_factors = [0.4, 0.6, 0.8, 0.9, 1.0]
        angle_offsets = [0.1, 0.2, 0.3, 0.4, 0.5]

        for layer in range(num_layers):
            layer_progress = min(1, (progress - 0.6) * 2.5 - layer * 0.2)
            if layer_progress > 0:
                current_size = size * size_factors[layer] * layer_progress
                num_petals = petal_counts[layer]
                angle_step = 2 * math.pi / num_petals

                layer_color = pygame.Color(color).lerp(
                    (255, 255, 255), 0.1 * layer)

                for i in range(num_petals):
                    angle = i * angle_step + angle_offsets[layer]
                    petal_x = x + math.cos(angle) * (current_size * 0.2)
                    petal_y = y - stem_height * 0.1 + \
                        math.sin(angle) * (current_size * 0.2)
                    draw_realistic_petal(surface, petal_x, petal_y,
                                         current_size, angle, layer_color, layer, layer_progress)


def draw_realistic_leaf(surface, x, y, size, angle, progress):
    """Dibuja una hoja realista con animación gradual"""
    points = []
    max_size = size * progress

    for t in range(0, 360, 5):
        theta = math.radians(t)
        rx = max_size * (0.5 + 0.3 * math.cos(2 * theta)) * math.cos(theta/2)
        ry = max_size * (0.5 + 0.3 * math.sin(2 * theta)) * math.sin(theta/2)

        rotated_x = rx * math.cos(angle) - ry * math.sin(angle)
        rotated_y = rx * math.sin(angle) + ry * math.cos(angle)
        points.append((int(x + rotated_x), int(y + rotated_y)))

    base_color = pygame.Color(LEAF_GREEN)
    shadow_color = base_color.lerp((0, 0, 0), 0.2)
    highlight_color = base_color.lerp((255, 255, 255), 0.1)

    pygame.draw.polygon(surface, base_color, points)
    pygame.draw.polygon(surface, shadow_color, points, 1)

    if progress > 0.5:
        for i in range(5):
            vx1 = x + (i - 2) * max_size * 0.1
            vy1 = y - max_size * 0.4
            vx2 = x + (i - 2) * max_size * 0.05
            vy2 = y + max_size * 0.4
            pygame.draw.line(surface, DARK_GREEN, (vx1, vy1), (vx2, vy2), 1)


def draw_text(surface, text, x, y, size, color, alpha):
    """Dibuja texto con transparencia"""
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_surface.set_alpha(int(alpha * 255))
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)


def main():
    heart_size = 0
    heart_growing = True
    rose_progress = 0.0
    text_phase = 0
    particles = []
    start_time = time.time()

    running = True
    while running:
        current_time = time.time() - start_time
        screen.fill(BACKGROUND)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Animación del corazón
        if heart_growing:
            if heart_size < 100:
                heart_size += 1
            else:
                heart_growing = False

        # Dibujar corazón
        draw_heart(screen, WIDTH//2, HEIGHT//3, heart_size, PINK)

        # Animación de las rosas (5 segundos)
        if not heart_growing:
            rose_progress = min(1.0, current_time / 5.0)

            # Posiciones de las rosas ajustadas
            draw_realistic_rose(screen, WIDTH//2 - 150,
                                HEIGHT//2 + 50, 80, ROSE_RED, rose_progress)
            draw_realistic_rose(screen, WIDTH//2 + 150,
                                HEIGHT//2 + 50, 80, ROSE_PINK, rose_progress)

            # Añadir texto gradualmente
            if rose_progress >= 1.0:
                if text_phase < 60:
                    text_phase += 1

                # Dibujar texto con efecto de fade in
                alpha = min(1.0, text_phase / 60.0)
                draw_text(screen, "Feliz San", WIDTH//2,
                          HEIGHT-200, 60, PINK, alpha)
                draw_text(screen, "Valentin", WIDTH//2,
                          HEIGHT-150, 72, PINK, alpha)

                # Añadir partículas brillantes
                if random.random() < 0.3:
                    particles.append({
                        'x': random.randint(0, WIDTH),
                        'y': random.randint(0, HEIGHT),
                        'size': random.randint(2, 4),
                        'life': 255
                    })

                # Actualizar y dibujar partículas
                for particle in particles[:]:
                    particle['life'] -= 2
                    if particle['life'] <= 0:
                        particles.remove(particle)
                    else:
                        color = (255, 182, 193, particle['life'])
                        pygame.draw.circle(screen, color,
                                           (int(particle['x']),
                                            int(particle['y'])),
                                           particle['size'])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
