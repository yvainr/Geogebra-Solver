import geogebra_html_generator
import triangle_drawer as triad
import task_parser as taskp
from math import *


# отрисовка треугольника по именам вершин
def triangle_from_task_drawer(A, B, C):

    AB = taskp.find_segment_with_points(A, B).size
    BC = taskp.find_segment_with_points(B, C).size
    CA = taskp.find_segment_with_points(C, A).size

    sides, sides_names = [BC, CA, AB], [f"{B}{C}", f"{C}{A}", f"{A}{B}"]

    CBA = taskp.find_angle_with_points(C, B, A).size
    ACB = taskp.find_angle_with_points(A, C, B).size
    BAC = taskp.find_angle_with_points(B, A, C).size

    if not CBA:
        try:
            CBA = 180 - taskp.find_angle_with_points(A, B, C).size
        except TypeError:
            pass
    if not ACB:
        try:
            ACB = 180 - taskp.find_angle_with_points(B, C, A).size
        except TypeError:
            pass
    if not BAC:
        try:
            BAC = 180 - taskp.find_angle_with_points(C, A, B).size
        except TypeError:
            pass

    angles, angles_names = [BAC, CBA, ACB], [f"{B}{A}{C}", f"{C}{B}{A}", f"{A}{C}{B}"]

    return triad.CreateTriangle(sides, angles, angles_names, sides_names)


def draw_polygon(points):
	ans = list()
	ans_polygon = 'Polygon('
	for point in points:
	    ans.append(f"{point.name}({triad.Equal(point.x)}, {triad.Equal(point.y)})")
	    ans_polygon += f"{point.name}, "
	ans_polygon = ans_polygon[:-2] + ')'
	ans.append(ans_polygon)
	geogebra_html_generator.insert_commands(ans)


def triangle_with_segment_synchronization(A, B, C, P1, P2):
    r = triad.DistanceBetweenPoints(P1, P2)

    for P in [A, B, C]:
        if P.name == P1.name:
            x, y = P.x, P.y
            P2.x -= P1.x; P2.y -= P1.y; A.x -= x; A.y -= y; B.x -= x; B.y -= y; C.x -= x; C.y -= y

    for P in [A, B, C]:
        if P.name == P2.name:
            phi = acos(P.x/r) - acos(P2.x/r)

    for P in [A, B, C]:
        if P1.name != P.name != P2.name:
            P3 = triad.MyPoint(P.x * cos(phi) - P.y * sin(phi), P.y * cos(phi) + P.x * sin(phi), P.name)

    P2.x += P1.x; P2.y += P1.y; P3.x += P1.x; P3.y += P1.y

    return P1, P2, P3


def text_splitter(text):
    taskp.points.clear()
    taskp.lines.clear()
    taskp.angles.clear()
    taskp.segments.clear()
    taskp.polygons.clear()

    text = text.replace('\r', '').split('\n')

    try:
        taskp.polygons_create(text[0])
        taskp.segments_create(text[1])
        taskp.angles_create(text[2])
        taskp.segments_relations_create(text[3])
        taskp.angles_relations_create(text[4])
        taskp.line_intersection_create(text[5])
    except IndexError:
        pass

    draw_polygon(triangle_from_task_drawer(taskp.polygons[0].points[0].name, taskp.polygons[0].points[1].name, taskp.polygons[0].points[2].name))