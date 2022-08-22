import geogebra_html_generator
import shapely.geometry
import ggb_drawer.triangle_drawer as td
import task_parser as tp
import normal_solver as ns
from math import *
from itertools import combinations, permutations
from objects_types import Objects
from random import uniform
from ggb_drawer.check_is_triangle_correct import check_triangle


def get_random_point_in_polygon(point_name, polygon):
    new_polygon = list()

    for point in polygon.points:
        new_polygon.append((point.x, point.y))
    poly = shapely.geometry.Polygon(new_polygon)
    minx, miny, maxx, maxy = poly.bounds

    while True:
        generated_point = shapely.geometry.Point(uniform(minx, maxx), uniform(miny, maxy))
        if poly.contains(generated_point):
            find_point = tp.find_point_with_name(point_name)
            find_point.x, find_point.y = generated_point.x, generated_point.y

            return find_point


def get_triangle_parameter(A, B, C):

    AB = tp.find_segment_with_points(A, B).size
    BC = tp.find_segment_with_points(B, C).size
    CA = tp.find_segment_with_points(C, A).size

    sides, sides_names = [BC, CA, AB], [f"{B}{C}", f"{C}{A}", f"{A}{B}"]

    CBA = tp.find_angle_with_points(C, B, A).size
    ACB = tp.find_angle_with_points(A, C, B).size
    BAC = tp.find_angle_with_points(B, A, C).size

    angles, angles_names = [BAC, CBA, ACB], [f"{B}{A}{C}", f"{C}{B}{A}", f"{A}{C}{B}"]

    return sides, angles, angles_names, sides_names


def draw_polygon(points, realize_data):
    ans_polygon = f'{tp.find_polygon_with_points(tp.get_points_names_from_list(points)).name}=Polygon('
    for point in points:
        realize_data.append(f"{point.name}({float(point.x.value)}, {float(point.y.value)})")
        ans_polygon += f"{point.name}, "
    ans_polygon = ans_polygon[:-2] + ')'
    realize_data.append(ans_polygon)
    for i in range(len(points)):
        seg = tp.find_segment_with_points(points[i].name, points[i-1].name)
        A, B = seg.points
        realize_data.append(f"{seg.name}=Segment({A.name}, {B.name})")
        realize_data.append(f"SetVisibleInView({seg.name}, 1, false)")


# def draw_specific_points(realize_data):
#     for point in tp.draw_data.points:
#         if point.specific_properties_point:
#             A = tp.find_point_with_name(point.specific_properties_triangle[0])
#             B = tp.find_point_with_name(point.specific_properties_triangle[1])
#             C = tp.find_point_with_name(point.specific_properties_triangle[2])
#
#             for draw_data in td.SpecificPointGeneration(point.name, point.specific_properties_point, A, B, C):
#                 realize_data.append(draw_data)


def triangle_with_segment_synchronization(A, B, C, P1, P2):
    r = td.DistanceBetweenPoints(P1, P2)

    for P in [A, B, C]:
        if P.name == P1.name:
            x, y = P.x, P.y
            P2.x -= P1.x; P2.y -= P1.y; A.x -= x; A.y -= y; B.x -= x; B.y -= y; C.x -= x; C.y -= y

    for P in [A, B, C]:
        if P.name == P2.name:
            phi = acos(P.x/r) - acos(P2.x/r)

    for P in [A, B, C]:
        if P1.name != P.name != P2.name:
            P3 = td.MyPoint(P.x * cos(phi) - P.y * sin(phi), P.y * cos(phi) + P.x * sin(phi), P.name)

    P2.x += P1.x; P2.y += P1.y; P3.x += P1.x; P3.y += P1.y

    return P1, P2, P3


def draw_lines_intersections(intersections, realize_data):
    if len(intersections) > 0:
        for intersection in intersections.split(','):
            l1 = f"Line({intersection.split()[0][0]}, {intersection.split()[0][1]})"
            l2 = f"Line({intersection.split()[1][0]}, {intersection.split()[1][1]})"
            point_name = intersection.split()[2]
            realize_data.append(f"{point_name}=Intersect({l1}, {l2})")


def create_polygon(vertices):
    if len(vertices) == 3:
        A, B, C = vertices

        # проверка треугольников
        check = check_triangle(*get_triangle_parameter(A, B, C)[:2])
        if check.__class__.__name__ == 'str':
            return check

        for points_with_cords in permutations(td.CreateTriangle(*get_triangle_parameter(A, B, C)), 3):
            if (A, B, C) == (points_with_cords[0].name, points_with_cords[1].name, points_with_cords[2].name):
                return points_with_cords

    if len(vertices) == 4:
        perspective_triangle = None
        perspective_current_size = 0
        for triangle in combinations(vertices, 3):
            triangle_parameter = get_triangle_parameter(triangle[0], triangle[1], triangle[2])
            perspective_size = 6 - triangle_parameter[0].count(None) - triangle_parameter[1].count(None)

            if perspective_size >= perspective_current_size:
                perspective_triangle = triangle

        A, B, C = td.CreateTriangle(get_triangle_parameter(perspective_triangle[0], perspective_triangle[1], perspective_triangle[2]))


def set_screen_size(realize_data):
    x_cords, y_cords = list(), list()

    for point in tp.solver_data.points:
        x_cords.append(point.x)
        y_cords.append(point.y)

    xmin = min(x_cords)
    ymin = min(y_cords)
    xmax = max(x_cords)
    ymax = max(y_cords)

    realize_data.append(f'ZoomIn({xmin - 0.25 * abs(xmin - xmax)}, {ymin - 0.25 * abs(ymin - ymax)}, {xmax + 0.25 * abs(xmin - xmax)}, {ymax + 0.25 * abs(ymin - ymax)})')


def text_splitter(text):
    realize_data = list()

    tp.task_data = Objects()
    tp.solver_data = Objects()

    text = text.replace('\r', '').split('\n')

    try:
        tp.polygons_create(text[0])
        tp.segments_create(text[1])
        tp.angles_create(text[2])
        tp.segments_relations_create(text[3])
        tp.angles_relations_create(text[4])
        tp.polygons_relations_create(text[5])
        tp.line_intersection_create(text[6])
        tp.questions_create(text[7])
    except IndexError:
        pass

    ns.solving_process()

    for polygon in text[0].split(','):
        ret = create_polygon(tp.get_points_names_from_list(tp.find_polygon_with_points(list(polygon.replace(' ', ''))).points))
        if type(ret) == str:
            return ret
        draw_polygon(ret, realize_data)

    for point in tp.solver_data.points:
        if point.in_polygon:
            get_random_point_in_polygon(point.name, point.in_polygon)
            realize_data.append(f'{point.name}({point.x}, {point.y})')

    # draw_specific_points(realize_data)

    try:
        draw_lines_intersections(text[6], realize_data)
    except IndexError:
        pass

    # set_screen_size(realize_data)

    geogebra_html_generator.insert_commands(realize_data)

    return 200
