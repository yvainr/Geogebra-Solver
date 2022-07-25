import geogebra_html_generator
import triangle_drawer as triad
import task_parser as taskp
from math import *
from itertools import combinations


def get_triangle_parameter(A, B, C):
    AB = taskp.find_segment_with_points(A, B).size
    BC = taskp.find_segment_with_points(B, C).size
    CA = taskp.find_segment_with_points(C, A).size

    sides, sides_names = [BC, CA, AB], [f"{B}{C}", f"{C}{A}", f"{A}{B}"]

    CBA = taskp.find_angle_with_points(C, B, A).size
    ACB = taskp.find_angle_with_points(A, C, B).size
    BAC = taskp.find_angle_with_points(B, A, C).size

    angles, angles_names = [BAC, CBA, ACB], [f"{B}{A}{C}", f"{C}{B}{A}", f"{A}{C}{B}"]

    return sides, angles, angles_names, sides_names


def draw_polygon(points, realize_data):
    ans_polygon = 'Polygon('
    for point in points:
        realize_data.append(f"{point.name}({triad.Equal(point.x)}, {triad.Equal(point.y)})")
        ans_polygon += f"{point.name}, "
    ans_polygon = ans_polygon[:-2] + ')'
    realize_data.append(ans_polygon)


def draw_specific_points(realize_data):
    for point in taskp.points:
        if point.specific_properties_point:
            A = taskp.find_point_with_name(point.specific_properties_triangle[0])
            B = taskp.find_point_with_name(point.specific_properties_triangle[1])
            C = taskp.find_point_with_name(point.specific_properties_triangle[2])

            for draw_data in triad.SpecificPointGeneration(point.name, point.specific_properties_point, A, B, C):
                realize_data.append(draw_data)


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

        return triad.CreateTriangle(*get_triangle_parameter(A, B, C))

    if len(vertices) == 4:
        perspective_triangle = None
        perspective_current_size = 0
        for triangle in combinations(vertices, 3):
            triangle_parameter = get_triangle_parameter(triangle[0], triangle[1], triangle[2])
            perspective_size = 6 - triangle_parameter[0].count(None) - triangle_parameter[1].count(None)

            if perspective_size >= perspective_current_size:
                perspective_triangle = triangle

        A, B, C = triad.CreateTriangle(get_triangle_parameter(perspective_triangle[0], perspective_triangle[1], perspective_triangle[2]))


def text_splitter(text):
    realize_data = list()

    taskp.points.clear()
    taskp.lines.clear()
    taskp.angles.clear()
    taskp.segments.clear()
    taskp.polygons.clear()
    taskp.facts.clear()
    taskp.questions.clear()

    text = text.replace('\r', '').split('\n')

    try:
        taskp.polygons_create(text[0])
        taskp.segments_create(text[1])
        taskp.angles_create(text[2])
        taskp.segments_relations_create(text[3])
        taskp.angles_relations_create(text[4])
        taskp.polygons_relations_create(text[5])
        taskp.line_intersection_create(text[6])
        taskp.questions_create(text[7])
    except IndexError:
        pass

    for polygon in taskp.polygons:
        try:
            taskp.UseRelations(taskp.segments)
            taskp.UseRelations(taskp.angles)
            ret = create_polygon(taskp.get_points_names_from_list(polygon.points))
            if type(ret) == str:
                return ret

            draw_polygon(ret, realize_data)
        except IndexError:
            pass

    draw_specific_points(realize_data)

    try:
        draw_lines_intersections(text[6], realize_data)
    except IndexError:
        pass

    geogebra_html_generator.insert_commands(realize_data)

    return 200
