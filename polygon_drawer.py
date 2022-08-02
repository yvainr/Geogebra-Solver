import geogebra_html_generator
import shapely.geometry
import triangle_drawer as triad
import task_parser as tp
from math import *
from itertools import combinations
from check_triangle import check_triangle
from objects_types import Objects


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
        realize_data.append(f"{point.name}({triad.Equal(point.x)}, {triad.Equal(point.y)})")
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
#             for draw_data in triad.SpecificPointGeneration(point.name, point.specific_properties_point, A, B, C):
#                 realize_data.append(draw_data)


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
        
        if type(check_triangle(get_triangle_parameter(A, B, C)[0], get_triangle_parameter(A, B, C)[1])) == str:
            return check_triangle(get_triangle_parameter(A, B, C)[0], get_triangle_parameter(A, B, C)[1])
        
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
        
        
def set_screen_size(realize_data):
    x_cords, y_cords = list(), list()

    for point in tp.drawer_data.points:
        x_cords.append(point.x)
        y_cords.append(point.y)

    realize_data.append(f'ZoomIn({min(x_cords) - 0.1 * abs(min(x_cords))}, {min(y_cords) - 0.1 * abs(min(y_cords))}, {max(x_cords) + 0.1 * abs(max(x_cords))}, {max(y_cords) + 0.1 * abs(max(y_cords))})')


def text_splitter(text):
  
    realize_data = list()

    tp.task_data = Objects()
    tp.drawer_data = Objects()
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

    for polygon in tp.drawer_data.polygons:
        try:
            tp.create_new_data_in_parser(tp.drawer_data.segments)
            tp.create_new_data_in_parser(tp.drawer_data.angles)
            ret = create_polygon(tp.get_points_names_from_list(polygon.points))
            if type(ret) == str:
                return ret

            draw_polygon(ret, realize_data)
        except IndexError:
            pass
        
    for point in tp.drawer_data.points:
        if point.in_polygon:
            get_random_point_in_polygon(point.name, point.in_polygon)
            realize_data.append(f'{point.name}({point.x}, {point.y})')

    # draw_specific_points(realize_data)

    try:
        draw_lines_intersections(text[6], realize_data)
    except IndexError:
        pass
    
    set_screen_size(realize_data)

    geogebra_html_generator.insert_commands(realize_data)

    return 200
