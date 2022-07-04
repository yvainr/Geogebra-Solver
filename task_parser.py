from fractions import Fraction
# для удобной работы с отношениями
# from itertools import combinations
# для всех сочетаний элементов из списка
from pprint import pprint
from copy import deepcopy


class Point:
    def __init__(self, name):
        self.name = name


class Line:
    def __init__(self, points_on_line={}):
        self.points = points_on_line


class Angle:
    def __init__(self, line_one, line_two, size=None, relations={}):
        self.lines = [line_one, line_two]
        self.size = size
        self.relations = relations


class Segment:
    def __init__(self, point_one, point_two, size=None, relations={}):
        self.points = {point_one, point_two}
        self.size = size
        self.relations = relations


class Polygon:
    def __init__(self, vertices, convex=True):
        self.points = vertices
        self.convex = convex
        # ?добавить точки внутри?


points = []
lines = []
angles = []
segments = []
polygons = []


def polygons_create(text):
    if len(text.split()) > 0:
        for polygon in text.split(','):
            vertices_list = list(polygon.split()[0])
            vertices_class_list = list()

            for vertice in vertices_list:
                vertices_class_list.append(find_point_with_name(vertice))

            if len(vertices_list) > 1:
                for vertice_index in range(len(vertices_list)):
                    find_segment_with_points(vertices_list[vertice_index-1], vertices_list[vertice_index])

            if len(vertices_list) > 3:
                try:
                    convex = polygon.split()[1]
                    if convex == 'выпуклый':
                        polygons.append(Polygon(vertices_class_list, False))
                    else:
                        polygons.append(Polygon(vertices_class_list))
                except IndexError:
                    polygons.append(Polygon(vertices_class_list))


def segments_create(text):
    if len(text.split()) > 0:
        for segment in text.split(','):
            segment = segment.split()
            try:
                size = int(segment[1])
            except IndexError:
                size = None

            seg = Segment(find_point_with_name(segment[0][0]), find_point_with_name(segment[0][1]), size)
            find_same_segments(segments, seg)


def angles_create(text):
    if len(text.split()) > 0:
        for angle in text.split(','):
            if len(angle) == 2:
                angle_name, angle_size = angle.split()
                A, B, C = list(angle_name)
                if A != B != C != A:
                    l1 = find_line_with_points(A, B)
                    l2 = find_line_with_points(B, C)
                    setattr(find_angle_with_lines(l1, l2), 'size', int(angle_size))
            if len(angle) == 3:
                l1, l2, angle_size = angle.split()
                l1 = find_line_with_points(l1[0], l1[1])
                l2 = find_line_with_points(l2[0], l2[1])
                setattr(find_angle_with_lines(l1, l2), 'size', int(angle_size))


def segments_relations_create(text):
    if len(text.split()) > 0:
        for relation in text.split(','):
            if len(relation.split()[0]) == len(relation.split()[1]) == 2:
                seg_1 = find_segment_with_points(relation.split()[0][0], relation.split()[0][1])
                seg_2 = find_segment_with_points(relation.split()[1][0], relation.split()[1][1])

            if len(relation.split()[0]) == 1:
                seg_1 = find_segment_with_points(relation.split()[0], relation.split()[1][0])
                seg_2 = find_segment_with_points(relation.split()[0], relation.split()[1][1])

                line = find_line_with_points(relation.split()[1][0], relation.split()[1][1])
                new_points = deepcopy(line.points)
                new_points.add(find_point_with_name(relation.split()[0]))
                setattr(line, 'points', new_points)

            if len(relation.split()[1]) == 1:
                seg_1 = find_segment_with_points(relation.split()[1], relation.split()[0][0])
                seg_2 = find_segment_with_points(relation.split()[1], relation.split()[0][1])

                line = find_line_with_points(relation.split()[0][0], relation.split()[0][1])
                new_points = deepcopy(line.points)
                new_points.add(find_point_with_name(relation.split()[1]))
                setattr(line, 'points', new_points)

            rel = relation.split()[2]
            new_relations = deepcopy(seg_1.relations)
            if seg_2 in new_relations:
                new_relations[seg_2] = Fraction(rel)
            else:
                new_relations.setdefault(seg_2, Fraction(rel))
            setattr(seg_1, 'relations', new_relations)

            new_relations = deepcopy(seg_2.relations)
            if seg_1 in new_relations:
                new_relations[seg_1] = 1/Fraction(rel)
            else:
                new_relations.setdefault(seg_1, 1/Fraction(rel))
            setattr(seg_2, 'relations', new_relations)


def angles_relations_create(text):
    if len(text.split()) > 0:
        for relation in text.split(','):
            ang_1, ang_2, rel = relation.split()
            ang_1 = find_angle_with_points(ang_1[0], ang_1[1], ang_1[2])
            ang_2 = find_angle_with_points(ang_2[0], ang_2[1], ang_2[2])

            new_relations = deepcopy(ang_1.relations)
            if ang_2 in new_relations:
                new_relations[ang_2] = Fraction(rel)
            else:
                new_relations.setdefault(ang_2, Fraction(rel))
            setattr(ang_1, 'relations', new_relations)

            new_relations = deepcopy(ang_2.relations)
            if ang_1 in new_relations:
                new_relations[ang_1] = 1/Fraction(rel)
            else:
                new_relations.setdefault(ang_1, 1/Fraction(rel))
            setattr(ang_2, 'relations', new_relations)


def line_intersection_create(text):
    if len(text.split()) > 0:
        for intersection in text.split(','):
            l1, l2, P = intersection.split()

            l1 = find_line_with_segment(find_segment_with_points(l1[0], l1[1]))
            if find_point_with_name(P) not in l1.points:
                new_points = deepcopy(l1.points)
                new_points.add(find_point_with_name(P))
                setattr(l1, 'points', new_points)

            l2 = find_line_with_segment(find_segment_with_points(l2[0], l2[1]))
            if find_point_with_name(P) not in l2.points:
                new_points = deepcopy(l2.points)
                new_points.add(find_point_with_name(P))
                setattr(l2, 'points', new_points)


# вспомогательная функция для поиска отрезка по вершинам, указываются имена точек
def find_segment_with_points(A, B):
    a = find_point_with_name(A)
    b = find_point_with_name(B)

    for seg in segments:
        if {a, b} == seg.points:
            return seg

    else:
        new_segment = Segment(a, b)
        segments.append(new_segment)
        return new_segment


# вспомогательная функция для поиска прямой по точкам на ней, указываются имена точек
def find_line_with_points(A, B):
    a = find_point_with_name(A)
    b = find_point_with_name(B)

    for line in lines:
        if {a, b} <= set(line.points):
            return line

    else:
        new_line = Line({a, b})
        lines.append(new_line)
        return new_line


# вспомогательная функция для поиска прямой по отрезку на ней
def find_line_with_segment(seg):
    A, B = seg.points
    return find_line_with_points(A.name, B.name)


# вспомогательная функция для поиска угла по прямым, его задающим
def find_angle_with_lines(l1, l2):
    for angle in angles:
        if [set(get_points_names_from_list(l1.points)), set(get_points_names_from_list(l2.points))] == [set(get_points_names_from_list(angle.lines[0].points)), set(get_points_names_from_list(angle.lines[1].points))]:
            return angle

    else:
        new_angle = Angle(l1, l2)
        angles.append(new_angle)
        return new_angle


# вспомогательная функция для поиска угла по точкам
def find_angle_with_points(A, B, C):
    l1 = find_line_with_points(A, B)
    l2 = find_line_with_points(B, C)

    for angle in angles:
        if angle.lines == [l1, l2]:
            return angle

    else:
        new_angle = Angle(l1, l2)
        angles.append(new_angle)
        return new_angle


# вспомогательная функция для поиска точки по её имени
def find_point_with_name(A):
    for point in points:
        if A == point.name:
            return point

    else:
        new_point = Point(A)
        points.append(new_point)
        return new_point


# вспомогательная функция для получения списка имен точек из списка
def get_points_names_from_list(points_list):
    ret = []
    for point in points_list:
        ret.append(point.name)

    return ret


def find_same_lines(lines_list, line):
    for lin in lines_list:
        if len(lin.points & line.points) >= 2:
            setattr(lin, 'points', lin.points | line.points)

    else:
        lines_list.append(line)


def find_same_segments(segments_list, segment):
    for seg in segments_list:
        if seg.points == segment.points:
            break

    else:
        segments_list.append(segment)


def find_same_angles(angles_list, angle):
    for ang in angles_list:
        if ang.lines == angle.lines:
            break

    else:
        angles_list.append(angle)


# модуль обработки данных при создании json
# вспомогательная функция для получения номеров объектов списка точек
def points_processing(points_list):
    ret = []
    for point in points_list:
        ret.append(f"object_{get_points_names_from_list(points).index(point.name)+1}")

    return ret


# вспомогательная функция для получения номеров объектов списка прямых
def lines_processing(lines_list):
    ret = []
    for line in lines_list:
        ret.append(f"object_{lines.index(line)+len(points)+1}")

    return ret


def relations_processing(relations_set, parametr):
    ret = {}
    for object in relations_set:
        if parametr == "angle":
            ret.setdefault(f"object_{relation_processing_helper_for_angles(object)+len(points)+len(lines)+1}", str(relations_set[object]))
        if parametr == "segment":
            ret.setdefault(f"object_{relation_processing_helper_for_segments(object)+len(points)+len(lines)+len(angles)+1}", str(relations_set[object]))

    return ret


def relation_processing_helper_for_segments(segment):
    for i in range(len(segments)):
        if set(get_points_names_from_list(segments[i].points)) == set(get_points_names_from_list(segment.points)):
            return i


def relation_processing_helper_for_angles(angle):
    for i in range(len(angles)):
        if set(get_points_names_from_list(angle.lines[0].points)) <= set(get_points_names_from_list(angles[i].lines[0].points)) and set(get_points_names_from_list(angle.lines[1].points)) <= set(get_points_names_from_list(angles[i].lines[1].points)):
            return i


# создание выходной json-ки
def json_create():
    output = {}
    object_index = 1

    for point in points:
        object = {}

        object.setdefault('name', point.name)
        object.setdefault('type', 'point')
        object.setdefault('points_on_object', None)
        object.setdefault('angle_between_lines', None)
        object.setdefault('size', None)
        object.setdefault('relations', None)
        object.setdefault('convex', None)

        output.setdefault(f"object_{object_index}", object)
        object_index += 1

    for line in lines:
        object = {}

        object.setdefault('name', None)
        object.setdefault('type', 'line')
        object.setdefault('points_on_object', points_processing(line.points))
        object.setdefault('angle_between_lines', None)
        object.setdefault('size', None)
        object.setdefault('relations', None)
        object.setdefault('convex', None)

        output.setdefault(f"object_{object_index}", object)
        object_index += 1

    for angle in angles:
        object = {}

        object.setdefault('name', None)
        object.setdefault('type', 'angle')
        object.setdefault('points_on_object', None)
        object.setdefault('angle_between_lines', lines_processing(angle.lines))
        object.setdefault('size', angle.size)
        object.setdefault('relations', relations_processing(angle.relations, 'angle'))
        object.setdefault('convex', None)

        output.setdefault(f"object_{object_index}", object)
        object_index += 1

    for segment in segments:
        object = {}

        object.setdefault('name', None)
        object.setdefault('type', 'segment')
        object.setdefault('points_on_object', points_processing(segment.points))
        object.setdefault('angle_between_lines', None)
        object.setdefault('size', segment.size)
        object.setdefault('relations', relations_processing(segment.relations, 'segment'))
        object.setdefault('convex', None)

        output.setdefault(f"object_{object_index}", object)
        object_index += 1

    for polygon in polygons:
        object = {}

        object.setdefault('name', None)
        object.setdefault('type', 'polygon')
        object.setdefault('points_on_object', points_processing(polygon.points))
        object.setdefault('angle_between_lines', None)
        object.setdefault('size', None)
        object.setdefault('relations', None)
        object.setdefault('convex', polygon.convex)

        output.setdefault(f"object_{object_index}", object)
        object_index += 1

    return output


# Волчкевич страница 26 задача 1
text1 = 'ABC'  # многоугольники
text2 = 'MB'  # дополнительные отрезки
text3 = 'CE BD -1'  # углы
text4 = 'AC M 1/1, AB M 1/1'  # отношения отрезков
text5 = 'MBA DBM 1/1, MBA CEM 1/1'  # отношения углов
text6 = 'CE BM E'  # точки пересечения прямых

polygons_create(text1)
segments_create(text2)
angles_create(text3)
segments_relations_create(text4)
angles_relations_create(text5)
line_intersection_create(text6)

pprint(json_create())
