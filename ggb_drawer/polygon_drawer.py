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
from ggb_drawer.useful_geometry_functions import PointOnCircle, CheckTrianglesIntersection
# from fact_description.detailed_fact_description import pretty_detailed_description


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
    poly = tp.find_polygon_with_points(points)
    poly.drawn = True
    ans_polygon = f'{poly.name}=Polygon('
    for point in points:
        point = tp.find_point_with_name(point)
        realize_data.append(f"{point.name}({float(point.x.value)}, {float(point.y.value)})")
        ans_polygon += f"{point.name}, "
    ans_polygon = ans_polygon[:-2] + ')'
    realize_data.append(ans_polygon)
    # for i in range(len(points)):
    #     seg = tp.find_segment_with_points(points[i], points[i-1])
    #     A, B = seg.points
    #     realize_data.append(f"{seg.name}=Segment({A.name}, {B.name})")
    #     realize_data.append(f'SetColor({seg.name}, "#1565C0")')
    #     realize_data.append(f"SetVisibleInView({seg.name}, 1, false)")


# def draw_specific_points(realize_data):
#     for point in tp.draw_data.points:
#         if point.specific_properties_point:
#             A = tp.find_point_with_name(point.specific_properties_triangle[0])
#             B = tp.find_point_with_name(point.specific_properties_triangle[1])
#             C = tp.find_point_with_name(point.specific_properties_triangle[2])
#
#             for draw_data in td.SpecificPointGeneration(point.name, point.specific_properties_point, A, B, C):
#                 realize_data.append(draw_data)


def triangle_with_point_synchronization(P, tr):
    x, y = P.x, P.y
    for point in tr:
        if point != P:
            point.x += P.x - x
            point.y += P.y - y

    return tr


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


def triangle_shift(A, B, C):
    phi = uniform(-pi, pi)
    vec = (cos(phi) * 2, sin(phi) * 2)

    if set(tp.get_points_names_from_list(tp.solver_data.polygons[0].points)) != {A.name, B.name, C.name}:
        while True:
            stop = True

            for polygon in tp.solver_data.polygons:
                if set(tp.get_points_names_from_list(polygon.points)) != {A.name, B.name, C.name}:

                    if CheckTrianglesIntersection(polygon.points, (A, B, C)):
                        A.x += vec[0]
                        A.y += vec[1]
                        B.x += vec[0]
                        B.y += vec[1]
                        C.x += vec[0]
                        C.y += vec[1]

                        stop = False
                        break

                else:
                    break

            if stop:
                break

    return A, B, C


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

        if [tp.find_point_with_name(A).x, tp.find_point_with_name(B).x, tp.find_point_with_name(C).x].count(None) == 3:
            A, B, C = triangle_shift(*td.CreateTriangle(*get_triangle_parameter(A, B, C)))

        # elif [tp.find_point_with_name(A).x, tp.find_point_with_name(B).x, tp.find_point_with_name(C).x].count(None) == 2:
        #     for point in [tp.find_point_with_name(A), tp.find_point_with_name(B), tp.find_point_with_name(C)]:
        #         if point.x:
        #             tr = td.CreateTriangle(*get_triangle_parameter(A, B, C))
        #             A, B, C = triangle_with_point_synchronization(point, tr)
        #             break

        else:
            return 'Solver error'

        for point in [A, B, C]:
            tp.find_point_with_name(point.name).save_cords(point.x, point.y)

    if len(vertices) == 4:
        perspective_triangle = None
        perspective_current_size = 0
        for triangle in combinations(vertices, 3):
            triangle_parameter = get_triangle_parameter(triangle[0], triangle[1], triangle[2])
            perspective_size = 6 - triangle_parameter[0].count(None) - triangle_parameter[1].count(None)

            if perspective_size >= perspective_current_size:
                perspective_triangle = triangle

        A, B, C = td.CreateTriangle(*get_triangle_parameter(perspective_triangle[0], perspective_triangle[1], perspective_triangle[2]))


def text_splitter(text):
    realize_data = list()

    tp.task_data = Objects()
    tp.solver_data = Objects()

    try:
        tasks, questions = text.replace('\r', '').split('\n')[:2]
    except ValueError:
        tasks, questions = text.replace('\r', '').split('\n')[0], ''

    for task in tasks.split(', '):
        ind = task.find(' ')
        task_type, task = task[:ind], task[ind + 1:]

        if task_type == 'poly':
            tp.polygons_create(task)
        elif task_type == 'seg':
            tp.segments_create(task)
        elif task_type == 'ang':
            tp.angles_create(task)
        elif task_type == 'seg_rel':
            tp.segments_relations_create(task)
        elif task_type == 'ang_rel':
            tp.angles_relations_create(task)
        elif task_type == 'poly_rel':
            tp.polygons_relations_create(task)
        elif task_type == 'lin_int':
            tp.line_intersection_create(task)
        elif task_type == 'p_str':
            tp.points_on_line_or_segment_create(task)
        elif task_type == 'p_poly':
            tp.points_in_polygon_create(task)
        elif task_type == 'p_seg_rel':
            tp.point_with_relation_on_segment_create(task)

    tp.questions_create(questions)

    solution = ns.solving_process()

    for task in tasks.split(', '):
        ind = task.find(' ')
        task_type, task = task[:ind], task[ind + 1:]

        if task_type == 'poly':
            err = create_polygon(list(task.replace(' ', '')))
            if err:
                return err
            draw_polygon(list(task.replace(' ', '')), realize_data)

        elif task_type == 'lin_int':
            draw_lines_intersections(task, realize_data)

        elif task_type == 'p_poly':
            for point in task.split('in')[0].split():
                point = tp.find_point_with_name(point)
                if point.in_polygon:
                    get_random_point_in_polygon(point, point.in_polygon)
                    realize_data.append(f'{point.name}({point.x}, {point.y})')

        elif task_type == 'p_seg_rel':
            segment = tp.find_segment_with_points(task[0], task[1])
            for point in segment.interior_points:
                point.x, point.y = (segment.points[0].x + segment.interior_points[point] * segment.points[1].x) / (
                        1 + segment.interior_points[point]), (
                                           segment.points[0].y + segment.interior_points[point] * segment.points[
                                       1].y) / (1 + segment.interior_points[point])
                realize_data.append(
                    f'{point.name}((x({segment.points[0].name}) + {segment.interior_points[point]} * x({segment.points[1].name})) / (1 + {segment.interior_points[point]}), (y({segment.points[0].name}) + {segment.interior_points[point]} * y({segment.points[1].name})) / (1 + {segment.interior_points[point]}))'
                )

    solution['ggb_commands'] = realize_data

    return solution
