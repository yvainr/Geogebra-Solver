from fractions import Fraction
# для удобной работы с отношениями
from itertools import combinations
from pprint import pprint
from copy import deepcopy


class Point:
    def __init__(self, name, cords=[]):
        self.name = name
        self.cords = cords


class Line:
    def __init__(self, points_on_line=[], name=None):
        self.points = points_on_line
        self.name = name


class Angle:
    def __init__(self, line_one, line_two, size=None, relations={}):
        self.lines = {line_one, line_two}
        self.size = size
        self.relations = relations


class Segment:
    def __init__(self, point_one, point_two, size=None, relations={}):
        self.points = {point_one, point_two}
        self.size = size
        self.relations = relations


points = []
lines = []
angles = []
segments = []

figure_types = {'параллелограмм', 'четырехугольник', 'прямоугольник', 'квадрат', 'треугольник',
                'равносторонний треугольник', 'равнобедренный треугольник', 'трапеция', 'ромб'}


def figure_analysis(text):
    # figure_description_example = "ABCD - квадрат"
    figure_description = text.split()
    point_names = list(figure_description[0])
    figure_type = figure_description[2]

    for point_name in point_names:
        points.append(Point(point_name))

    for segment_name in list(combinations(points, 2)):
        segments.append(Segment(segment_name[0], segment_name[1]))

    for point_name in list(combinations(points, 2)):
        lines.append(Line([point_name[0], point_name[1]]))

    for line_name in list(combinations(lines, 2)):
        angles.append(Angle(line_name[0], line_name[1]))

    # вот здесь генерируются по точкам прямые через них, отрезки и углы между всеми парами прямых

    figure_sides = []

    for i in range(len(point_names)):
        segment = find_segment_with_points(point_names[i - 1], point_names[i])
        figure_sides.append(segment)

    # формируем массив всех сторон фигуры

    if len(point_names) == 4:
        if figure_type == 'квадрат':

            for side_1 in figure_sides:
                for side_2 in figure_sides:
                    if get_points_names_from_list(side_1.points) != get_points_names_from_list(side_2.points):
                        side_1_copy = deepcopy(side_1.relations)
                        side_1_copy.setdefault(side_2, 1)
                        setattr(side_1, 'relations', side_1_copy)

            # говорим, что каждый отрезок относится как 1 к 1 с остальными

            for i in range(len(figure_sides)):
                line_through_side_1 = find_line_with_segment(figure_sides[i-1])
                line_through_side_2 = find_line_with_segment(figure_sides[i])
                angle = find_angle_with_lines(line_through_side_1, line_through_side_2)
                angle.size = 90

            # говорим, что углы между соседними прямыми, проходящими через отрезки, по 90

        if figure_type == 'прямоугольник':

            figure_sides[0].relations.setdefault(figure_sides[2], 1)
            figure_sides[2].relations.setdefault(figure_sides[0], 1)
            figure_sides[1].relations.setdefault(figure_sides[3], 1)
            figure_sides[3].relations.setdefault(figure_sides[1], 1)

            # говорим, что противоположные отрезки относятся как 1 к 1 с остальными

            for i in range(len(figure_sides)):
                line_through_side_1 = find_line_with_segment(figure_sides[i-1])
                line_through_side_2 = find_line_with_segment(figure_sides[i])
                angle = find_angle_with_lines(line_through_side_1, line_through_side_2)
                angle.size = 90

        if figure_type == 'ромб':
            pass

        if figure_type == 'трапеция':
            pass

        if figure_type == 'дельтоид':
            pass

        if figure_type == 'параллелограмм':
            pass

            # говорим, что углы между соседними прямыми, проходящими через отрезки, по 90


# вспомогательная функция для поиска отрезка по вершинам, указываются имена точек
def find_segment_with_points(a, b):
    A = find_point_with_name(a)
    B = find_point_with_name(b)

    for segment in segments:
        if {A, B} == segment.points:
            return segment

    else:
        return None


# вспомогательная функция для поиска прямой по точкам на ней, указываются именя точек
def find_line_with_points(a, b):
    A = find_point_with_name(a)
    B = find_point_with_name(b)

    for line in lines:
        if {A, B} <= set(line.points):
            return line

    else:
        return None


# вспомогательная функция для поиска прямой по отрезку на ней
def find_line_with_segment(seg):
    A, B = seg.points
    return find_line_with_points(A.name, B.name)


# вспомогательная функция для поиска угла по прямым, его задающим
def find_angle_with_lines(l1, l2):
    for angle in angles:
        if {l1, l2} == angle.lines:
            return angle

    else:
        return None


# вспомогательная функция для поиска точки по её имени
def find_point_with_name(A):
    for point in points:
        if A == point.name:
            return point

    else:
        return None


# вспомогательная функция для получения списка имен точек из списка
def get_points_names_from_list(points_list):
    ret = set()
    for point in points_list:
        ret.add(point.name)

    return ret


# вспомогательная функция для получения номеров объектов списка точек
def points_processing(points_list):
    ret = []
    for point in points_list:
        ret.append(f"object_{points.index(point)+1}")

    return ret


# вспомогательная функция для получения номеров объектов списка прямых
def lines_processing(lines_list):
    ret = []
    for line in lines_list:
        ret.append(f"object_{lines.index(line)+len(points)+1}")

    return ret


# вспомогательная функция для поиска индекса отрезка в списке
def find_segment_index_in_list(segment):
    for i in range(len(segments)):
        if get_points_names_from_list(segments[i].points) == get_points_names_from_list(segment.points):
            return i

    else:
        return None


def relations_processing(relations_set, par):
    ret = {}
    for object in relations_set:
        if par == "angle":
            ret.setdefault(f"object_{angles.index(object)+len(points)+len(lines)+1}", relations_set[object])
        if par == "segment":
            ret.setdefault(f"object_{find_segment_index_in_list(object)+len(points)+len(lines)+len(angles)+1}", relations_set[object])

    return ret


# создание выходной json-ки
def create_output():
    output = {}
    object_index = 1

    for point in points:
        object = {}

        object.setdefault('name', point.name)
        object.setdefault('type', 'point')
        object.setdefault('points_on_line', None)
        object.setdefault('points_on_segment', None)
        object.setdefault('cords', point.cords)
        object.setdefault('angle_between_lines', None)
        object.setdefault('size', None)
        object.setdefault('relations', None)

        output.setdefault(f"object_{object_index}", object)
        object_index += 1

    for line in lines:
        object = {}

        object.setdefault('name', line.name)
        object.setdefault('type', 'line')
        object.setdefault('points_on_line', points_processing(line.points))
        object.setdefault('points_on_segment', None)
        object.setdefault('cords', None)
        object.setdefault('angle_between_lines', None)
        object.setdefault('size', None)
        object.setdefault('relations', None)

        output.setdefault(f"object_{object_index}", object)
        object_index += 1

    for angle in angles:
        object = {}

        object.setdefault('name', None)
        object.setdefault('type', 'angle')
        object.setdefault('points_on_line', None)
        object.setdefault('points_on_segment', None)
        object.setdefault('cords', None)
        object.setdefault('angle_between_lines', lines_processing(angle.lines))
        object.setdefault('size', angle.size)
        object.setdefault('relations', relations_processing(angle.relations, 'angle'))

        output.setdefault(f"object_{object_index}", object)
        object_index += 1

    for segment in segments:
        object = {}

        object.setdefault('name', None)
        object.setdefault('type', 'segment')
        object.setdefault('points_on_line', None)
        object.setdefault('points_on_segment', points_processing(segment.points))
        object.setdefault('cords', None)
        object.setdefault('angle_between_lines', None)
        object.setdefault('size', segment.size)
        object.setdefault('relations', relations_processing(segment.relations, 'segment'))

        output.setdefault(f"object_{object_index}", object)
        object_index += 1

    return output


def find_same_lines():
    for i in range(len(lines)-1):
        l1_points = get_points_names_from_list(lines[i].points)
        for j in range(i+1, len(lines)):
            l2_points = get_points_names_from_list(lines[j].points)
            if len(l1_points & l2_points) >= 2:
                pass


json_example = \
    {
        'name': 'a',
        'class': 'Segment',
        'points_on_line': None,
        # only lines
        'points_on_segment': {'A', 'B'},
        # only segments
        'cords': None,
        # only points
        'angle_between_lines': {},
        # only angles
        'size': 7,
        # only segments and angles
        'relations': {'object_name': Fraction(1, 3)}
        # only segments
    }

text = 'ABCD - квадрат'
figure_analysis(text)

pprint(create_output())