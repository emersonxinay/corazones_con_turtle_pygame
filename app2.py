import turtle
import time
import math
import random

# Configuración inicial
screen = turtle.Screen()
screen.setup(1280, 720)
screen.bgcolor('#0a0a1a')
screen.title('Corazón y Rosas')
turtle.hideturtle()
screen.tracer(0)


def ease_out_cubic(x):
    """Función de suavizado cúbica para una animación más natural"""
    return 1 - pow(1 - x, 3)


def dibujar_corazon(x, y, tamaño):
    """Dibuja un corazón completo usando ecuaciones paramétricas"""
    turtle.clear()
    turtle.penup()
    turtle.color('#FF1493')  # Rosa brillante
    turtle.begin_fill()

    # Dibujamos el corazón punto por punto
    puntos = []
    for t in range(360):  # Cambiado a 360 para un círculo completo
        theta = math.radians(t)
        # Ecuaciones paramétricas corregidas
        px = 16 * math.sin(theta) ** 3
        py = 13 * math.cos(theta) - 5 * math.cos(2*theta) - \
            2 * math.cos(3*theta) - math.cos(4*theta)
        puntos.append((x + px * tamaño/16, y + py * tamaño/13))

    # Dibujamos el corazón
    turtle.goto(puntos[0])
    turtle.pendown()
    for px, py in puntos:
        turtle.goto(px, py)

    turtle.end_fill()
    screen.update()


def dibujar_hoja_rosa(tamaño):
    """Dibuja una hoja elegante de rosa"""
    turtle.begin_fill()
    turtle.forward(tamaño)
    turtle.right(45)
    for _ in range(15):
        turtle.right(3)
        turtle.forward(tamaño/15)
    turtle.right(45)
    turtle.forward(tamaño)
    turtle.end_fill()


def dibujar_petalo_rosa(tamaño, angulo_curva):
    """Dibuja un pétalo de rosa con curva ajustable"""
    turtle.begin_fill()
    for _ in range(2):
        turtle.circle(tamaño, angulo_curva)
        turtle.left(180 - angulo_curva)
    turtle.end_fill()


def dibujar_rosa(x, y, escala):
    """Dibuja una rosa con pétalos en espiral"""
    # Tallo
    turtle.penup()
    turtle.goto(x, y - 200 * escala)
    turtle.setheading(90)
    turtle.pensize(4)
    turtle.color('#2F8B57')
    turtle.pendown()

    # Animar crecimiento del tallo
    altura_actual = 0
    for i in range(100):
        turtle.forward(2 * escala)
        turtle.right(math.sin(i/10) * 2)
        altura_actual += 2 * escala

        # Añadir hojas
        if altura_actual in [40, 80, 120, 160]:
            pos = turtle.position()
            heading = turtle.heading()

            # Hojas a ambos lados
            for angulo in [-40, 40]:
                turtle.color('#2F8B22')  # Verde para las hojas
                turtle.setheading(heading + angulo)
                dibujar_hoja_rosa(30 * escala)
                turtle.penup()
                turtle.goto(pos)
                turtle.setheading(heading)
                turtle.pendown()

            turtle.color('#2F8B57')

        screen.update()
        time.sleep(0.01)

    # Posición final para la flor
    pos_final = turtle.position()

    # Centro de la rosa
    turtle.penup()
    turtle.goto(pos_final)

    # Pétalos en espiral
    # Diferentes tonos de rosa
    colores_rosa = ['#FF69C4', '#FF1493', '#DC7093']
    tamaño_inicial = 10 * escala

    # Pétalos internos (más pequeños y cerrados)
    for i in range(15):
        turtle.penup()
        turtle.goto(pos_final)
        turtle.setheading(i * 25)
        turtle.color(colores_rosa[i % 3])
        dibujar_petalo_rosa(tamaño_inicial + i * escala, 60)
        screen.update()
        time.sleep(0.05)

    # Pétalos externos (más grandes y abiertos)
    for i in range(15):
        turtle.penup()
        turtle.goto(pos_final)
        turtle.setheading(i * 25 + 10)
        turtle.color(colores_rosa[(i + 1) % 3])
        dibujar_petalo_rosa(tamaño_inicial + (i + 15) * escala, 90)
        screen.update()
        time.sleep(0.05)


def escribir_texto_animado(mensaje, y_pos, tamaño, color):
    """Escribe texto con animación elegante sin borrar elementos anteriores"""
    turtle.penup()
    turtle.color(color)

    # Calculamos el ancho total para centrar
    ancho_letra = tamaño * 0.6
    x_inicio = -(len(mensaje) * ancho_letra) / 2

    # Creamos un nuevo turtle solo para el texto
    texto_turtle = turtle.Turtle()
    texto_turtle.hideturtle()
    texto_turtle.penup()
    texto_turtle.color(color)

    for i, letra in enumerate(mensaje):
        x = x_inicio + (i * ancho_letra)
        # Efecto de aparecer desde abajo
        for y in range(int(y_pos - 50), int(y_pos + 1), 2):
            texto_turtle.clear()  # Solo limpia el texto, no toda la pantalla

            # Dibujamos las letras ya completadas
            for j in range(i):
                texto_turtle.goto(x_inicio + (j * ancho_letra), y_pos)
                texto_turtle.write(mensaje[j], align="center",
                                   font=("Courier", tamaño, "bold"))

            # Dibujamos la letra actual subiendo
            texto_turtle.goto(x, y)
            texto_turtle.write(letra, align="center",
                               font=("Courier", tamaño, "bold"))

            screen.update()
            time.sleep(0.01)

        screen.update()
        time.sleep(0.1)


def animacion_principal():
    """Secuencia principal de animación"""
    # Animar corazón creciente
    for i in range(100):
        progress = i / 99
        tamaño_suavizado = ease_out_cubic(progress) * 150
        dibujar_corazon(0, 50, tamaño_suavizado)
        time.sleep(0.02 - (0.015 * progress))

    time.sleep(0.5)

    # Dibujar dos rosas
    dibujar_rosa(-150, 0, 0.8)
    time.sleep(0.3)
    dibujar_rosa(150, 0, 0.8)

    time.sleep(0.5)

    # Añadir texto animado sin borrar lo anterior
    escribir_texto_animado("Feliz", -200, 36, '#FF69B4')
    time.sleep(0.3)
    escribir_texto_animado("San Valentin", -250, 48, '#FF1493')

    # Efecto final de brillo manteniendo todo visible
    for _ in range(30):
        x = random.randint(-300, 300)
        y = random.randint(-300, 300)
        turtle.penup()
        turtle.goto(x, y)
        turtle.color('#FFB6C1')
        turtle.dot(random.randint(2, 5))
        screen.update()
        time.sleep(0.05)


# Ejecutar animación
animacion_principal()
turtle.done()
