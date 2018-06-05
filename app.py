#  from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import matplotlib.pylab as plt
import math
import random
from flask import Flask, render_template, request, send_file, redirect, url_for
from PIL import Image, ImageDraw
import io

app = Flask(__name__)


@app.route('/')   # Главная страница
def home():
    return render_template('index.html')


@app.route('/result')  # Страница с результатом после запроса
def fractal_page():
        return render_template('fractal.html')


@app.route('/fractal', methods=['POST'])
def make_fractal():                                  # Функция для выбора изображения
    lev = request.form.get("Level")
    typ = request.form.get('Figure_Type')
    depth = int(lev)
    fig = plt.figure(figsize=(25,20))

    if request.form.get("Level") is None or depth < 0:
        return render_template("error.html")

    if typ == "Fractal Tree":    # Фрактальное дерево
        fractal_tree(11, 9, 90, depth)
        s = "Fractal Tree (iterations = %i)" % depth
        plt.title(s, fontsize=35)
    elif typ == "Sierpinski Triangle":  # Треугольник Серпинского
        a = np.array([0, 0])
        b = np.array([1, 0])
        c = np.array([0.5, np.sqrt(3) / 2.])
        fig = plt.figure(figsize=(25, 25))

        sierpinski_triangle(a, b, c, depth)

        plt.title("Sierpinski Triangle (iterations =" + lev + ")", fontsize=35)
        plt.axis('equal')

    elif typ == "Koch Line":    # Треугольник Коха
        fig = plt.figure(figsize=(25, 7))

        plt.title("Koch Line (iterations = " + lev + ")", fontsize=35)
        points = koch(a=np.array([0, 0]), b=np.array([1, 0]), iterations=depth)
        ptsx = []
        ptsy = []
        for i in range(len(points)):
            ptsx.append(points[i][0])
            ptsy.append(points[i][1])
            plt.plot(ptsx, ptsy, '-')
            plt.axis('equal')
    else:                   # Снежинка Коха
        h = np.sqrt(3) / 2.

        points1 = koch(a=np.array([0, 0]), b=np.array([1, 0]), iterations=depth)
        points2 = koch(a=np.array([1, 0]), b=np.array([0.5, -h]), iterations=depth)
        points3 = koch(a=np.array([0.5, -h]), b=np.array([0, 0]), iterations=depth)

        points = []
        for i in range(len(points1)):
            points.append(np.array(points1[i]))
        for i in range(len(points2)):
            points.append(np.array(points2[i]))
        for i in range(len(points3)):
            points.append(np.array(points3[i]))

        ptsx = []
        ptsy = []
        for i in range(len(points)):
            ptsx.append(points[i][0])
            ptsy.append(points[i][1])

        fig = plt.figure(figsize=(25, 25))
        plt.title("Koch Triangle (iterations = " + lev + ")", fontsize=30)
        plt.plot(ptsx, ptsy, '-')
        plt.fill(ptsx, ptsy, color='#FF7F50', alpha=0.7)
        plt.axis('equal')

    plt.axis('off')

    img_data = io.BytesIO()
    FigureCanvas(fig).print_png(img_data)
    img_data.seek(0)
    return send_file(img_data, mimetype='image/png')

    #return render_template("fractal.html", filename=filename)
    #return send_file(filename, mimetype='image/png')'''


def fractal_tree(x1, y1, angle, depth):
    if depth > 0:
        x2 = x1 + int(math.cos(math.radians(angle)) * depth * 10.0)
        y2 = y1 + int(math.sin(math.radians(angle)) * depth * 10.0)
        plt.plot([x1, x2], [y1, y2], '-', color='blue', lw=3)
        fractal_tree(x2, y2, angle - 20, depth - 1)
        fractal_tree(x2, y2, angle + 20, depth - 1)


def sierpinski_triangle(a, b, c, iterations):
    '''
    Recursively generated Sierpinski Triangle.
    '''
    if iterations == 0:
        # Fill the triangle with vertices a, b, c.
        plt.fill([a[0], b[0], c[0]], [a[1], b[1], c[1]], 'g')
        #plt.hold(True)
    else:
        # Recursive calls for the three subtriangles.
        sierpinski_triangle(a, (a + b) / 2., (a + c) / 2., iterations - 1)
        sierpinski_triangle(b, (b + a) / 2., (b + c) / 2., iterations - 1)
        sierpinski_triangle(c, (c + a) / 2., (c + b) / 2., iterations - 1)


def koch(a, b, iterations):
    a1 = a[0]
    a2 = a[1]

    b1 = b[0]
    b2 = b[1]

    theta = np.arctan((b2 - a2) / (b1 - a1))
    length = np.sqrt((a1 - b1) ** 2 + (a2 - b2) ** 2)

    c1 = (2 * a1 + b1) / 3.
    c2 = (2 * a2 + b2) / 3.
    c = [c1, c2]

    d1 = (a1 + 2 * b1) / 3.
    d2 = (a2 + 2 * b2) / 3.
    d = [d1, d2]

    if c1 >= a1:
        m1 = c1 + (length / 3.) * math.cos(theta + math.pi / 3.)
        m2 = c2 + (length / 3.) * math.sin(theta + math.pi / 3.)
    else:
        m1 = c1 + (length / 3.) * math.cos(theta - 2 * math.pi / 3.)
        m2 = c2 + (length / 3.) * math.sin(theta - 2 * math.pi / 3.)
    m = [m1, m2]

    c = np.array(c)
    d = np.array(d)
    m = np.array(m)

    points = []

    if iterations == 0:
        points.extend([a, b])
    elif iterations == 1:
        points.extend([a, c, m, d, b])
    else:
        points.extend(koch(a, c, iterations - 1))
        points.extend(koch(c, m, iterations - 1))
        points.extend(koch(m, d, iterations - 1))
        points.extend(koch(d, b, iterations - 1))

    return points


""" ещё 2 метода для фракталов + поменять названия в хтмл!!!"""

if __name__ == '__main__':
    app.run(debug=True)
