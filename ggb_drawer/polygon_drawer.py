from ggb_html_generator.geogebra_html_generator import insert_commands
import shapely.geometry
import ggb_drawer.triangle_drawer as td
from ggb_data_processing import task_parser as tp
import ggb_solver.normal_solver as ns
from math import *
from itertools import combinations
from ggb_data_processing.objects_types import Objects
from random import uniform
from ggb_drawer.check_is_triangle_correct import check_triangle
from ggb_data_processing.objects_types import Size
from ggb_drawer.useful_geometry_functions import PointOnCircle


def check_is_point_in_polygon(find_point, polygon):
    new_polygon = list()

    for point in polygon.points:
        new_polygon.append((point.x, point.y))

    poly = shapely.geometry.Polygon(new_polygon)

    if find_point.x:
        return poly.contains(shapely.geometry.Point(find_point.x, find_point.y))
    return False


def get_random_point_in_polygon(find_point, polygon):
    new_polygon = list()

    for point in polygon.points:
        new_polygon.append((point.x, point.y))

    poly = shapely.geometry.Polygon(new_polygon)
    minx, miny, maxx, maxy = poly.bounds

    if (not find_point.x and check_is_point_in_polygon(find_point, polygon)) or find_point.x:
        return find_point

    while True:
        generated_point = shapely.geometry.Point(uniform(minx, maxx), uniform(miny, maxy))
        if poly.contains(generated_point):
            find_point.x, find_point.y = Size(generated_point.x), Size(generated_point.y)

            return find_point


def get_triangle_parameter(A, B, C):
    AB = tp.find_segment_with_points(A, B)
    BC = tp.find_segment_with_points(B, C)
    CA = tp.find_segment_with_points(C, A)

    CBA = tp.find_angle_with_points(C, B, A)
    ACB = tp.find_angle_with_points(A, C, B)
    BAC = tp.find_angle_with_points(B, A, C)

    return [BC, CA, AB], [BAC, CBA, ACB], [f"{B}{C}", f"{C}{A}", f"{A}{B}"], [f"{B}{A}{C}", f"{C}{B}{A}", f"{A}{C}{B}"]


def draw_polygon(points, realize_data):
    ans_polygon = f'{tp.find_polygon_with_points(points).name}=Polygon('
    for point in points:
        point = tp.find_point_with_name(point)
        realize_data.append(f"{point.name}({float(point.x.value)}, {float(point.y.value)})")
        ans_polygon += f"{point.name}, "
    ans_polygon = ans_polygon[:-2] + ')'
    realize_data.append(ans_polygon)
    for i in range(len(points)):
        seg = tp.find_segment_with_points(points[i], points[i-1])
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
            P3 = (P.x * cos(phi) - P.y * sin(phi), P.y * cos(phi) + P.x * sin(phi), P.name)

    P3[0] += P1.x
    P3[1] += P1.y

    return P3


def draw_lines_intersections(intersections, realize_data):
    if len(intersections) > 0:
        for intersection in intersections.split(','):
            l1 = f"Line({intersection.split()[0][0]}, {intersection.split()[0][1]})"
            l2 = f"Line({intersection.split()[1][0]}, {intersection.split()[1][1]})"
            point_name = intersection.split()[2]
            realize_data.append(f"{point_name}=Intersect({l1}, {l2})")


def create_polygon(vertices):
    if len(vertices) == 2:
        AB = tp.find_segment_with_points(vertices[0], vertices[1])
        A, B = AB.points

        if not AB.size:
            AB.size = uniform(3, 6)

        if A.x and not B.x:
            B.x, B.y = PointOnCircle(A, AB.size)
            if B.in_polygon:
                for t in range(2000):
                    if not check_is_point_in_polygon(B, B.in_polygon):
                        B.x, B.y = PointOnCircle(A, AB.size)
                    else:
                        break

        if B.x and not A.x:
            A.x, A.y = PointOnCircle(B, AB.size)
            if A.in_polygon:
                for t in range(2000):
                    if not check_is_point_in_polygon(A, A.in_polygon):
                        A.x, A.y = PointOnCircle(B, AB.size)
                    else:
                        break

    if len(vertices) == 3:
        A, B, C = vertices

        # проверка треугольников
        check = check_triangle(get_triangle_parameter(A, B, C)[:2])
        if check.__class__.__name__ == 'str':
            return check

        td.CreateTriangle(*get_triangle_parameter(A, B, C))

    if len(vertices) == 4:
        perspective_triangle = None
        perspective_current_size = 0
        for triangle in combinations(vertices, 3):
            triangle_parameter = get_triangle_parameter(triangle[0], triangle[1], triangle[2])
            perspective_size = 6 - triangle_parameter[0].count(None) - triangle_parameter[1].count(None)

            if perspective_size >= perspective_current_size:
                perspective_triangle = triangle

        A, B, C = td.CreateTriangle(*get_triangle_parameter(perspective_triangle[0], perspective_triangle[1], perspective_triangle[2]))


def text_splitter(text):  # def text_splitter(text, input_file_name):
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
        tp.points_on_line_or_segment_create(text[7])
        tp.points_in_polygon_create(text[8])
        tp.questions_create(text[9])
    except IndexError:
        pass

    solution = ns.solving_process()

    for polygon in text[0].split(','):
        err = create_polygon(list(polygon.replace(' ', '')))
        if type(err) == str:
            return err

        draw_polygon(list(polygon.replace(' ', '')), realize_data)

    for point in tp.solver_data.points:
        if point.in_polygon:
            get_random_point_in_polygon(point, point.in_polygon)
            realize_data.append(f'{point.name}({point.x}, {point.y})')

    # draw_specific_points(realize_data)

    try:
        draw_lines_intersections(text[6], realize_data)
    except IndexError:
        pass

    # set_screen_size(realize_data)

    # insert_commands(realize_data, input_file_name=input_file_name)

    solution['ggb_commands'] = realize_data

    return solution
