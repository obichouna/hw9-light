import math
from display import *

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    color = [0, 0, 0]
    amb = calculate_ambient(ambient, areflect)
    diff = calculate_diffuse(light, dreflect, normal)
    spec = calculate_specular(light, sreflect, view, normal)
    i = 0
    while (i < 3):
        color[i] = amb[i] + diff[i] + spec[i]
        i = i + 1
    return color

def calculate_ambient(alight, areflect):
    var = [0, 0, 0]
    for i in range(len(alight)):
        var[i] = int(alight[i] * areflect[i])
        var[i] = limit_color(var[i])
    return var

def calculate_diffuse(light, dreflect, normal):
    var = [0, 0, 0]
    p = light[COLOR]
    l = light[LOCATION]
    n = normal
    normalize(l)
    normalize(n)
    for i in range(len(dreflect)):
        var[i] = int(p[i] * dreflect[i] * dot_product(l, n))
        var[i] = limit_color(var[i])
    return var

def calculate_specular(light, sreflect, view, normal):
    p = light[COLOR]
    l = light[LOCATION]
    n = normal
    v = view
    normalize(n)
    normalize(v)
    normalize(l)
    var = [0, 0, 0]
    ans = [0, 0, 0]
    for x in range(3):
        var[x] = 2 * dot_product(n, l) * n[x]
        var[x] -= l[x]
        ans[x] = p[x] * sreflect[x]
    for x in range(3):
        ans[x] *= (dot_product(var, v))**SPECULAR_EXP
        ans[x] = int(ans[x])
        ans[x] = limit_color(ans[x])
    return ans

def limit_color(color):
    if color < 0:
        color = 0
    if color > 255:
        color = 255
    return color

#vector functions
def normalize(vector):
    var = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
    for i in range(3):
        vector[i] = vector[i] / var

def dot_product(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]

def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
