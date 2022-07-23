from fractions import Fraction
from pprint import pprint
from random import uniform


class Point:
    def __init__(self,
                 name,
                 specific_properties_point=None,
                 specific_properties_triangle=None,
                 cord_x=None,
                 cord_y=None):
        self.name = name
        self.specific_properties_point = specific_properties_point
        self.specific_properties_triangle = specific_properties_triangle
        self.x = cord_x
        self.y = cord_y

    def __str__(self):
        return f'name: {self.name}, specific_properties_point: {self.specific_properties_point}, specific_properties_triangle: {self.specific_properties_triangle}, x: {self.x}, y: {self.y}'


class Line:
    def __init__(self,
                 points):
        self.points = points

    def __str__(self):
        return f'points: {get_points_names_from_list(self.points)}'


class Angle:
    def __init__(self,
                 line_one,
                 line_two,
                 size=None):
        self.lines = [line_one, line_two]
        self.size = size
        self.relations = dict()

    def __str__(self):
        str_lines = ''
        str_relations = ''

        for line in self.lines:
            str_lines += f' {get_points_names_from_list(line.points)}'

        for rel in self.relations:
            str_relations += f'{get_points_names_from_list(rel.lines[0].points)} {get_points_names_from_list(rel.lines[1].points)} {self.relations[rel]} '

        if not str_relations:
            str_relations = 'None '

        return f'lines:{str_lines}, size: {self.size}, relations: {str_relations}'


class Segment:
    def __init__(self,
                 point_one,
                 point_two,
                 size=None):
        self.points = {point_one, point_two}
        self.size = size
        self.relations = dict()

    def __str__(self):
        str_relations = ''

        for rel in self.relations:
            str_relations += f'{get_points_names_from_list(rel.points)}: {self.relations[rel]} '

        if not str_relations:
            str_relations = 'None '

        return f'points: {get_points_names_from_list(self.points)}, size: {self.size}, relations: {str_relations}'


class Polygon:
    def __init__(self,
                 vertices,
                 convex=True):
        self.points = vertices
        self.convex = convex
        self.relations = dict()
        # ?добавить точки внутри?

    def __str__(self):
        return f'points: {get_points_names_from_list(self.points)}, convex: {self.convex}'


class Fact:
    def __init__(self,
                 id,
                 generation,
                 fact_type,
                 objects,
                 value=None,
                 question=False
                 ):
        self.id = id
        self.generation = generation  # ступень дерева
        self.fact_type = fact_type  # relation (отношение), size (значение)
        self.objects = objects
        self.value = value
        self.question = question
        self.description = str()
        self.root_facts = list()  # список фактов-причин
        self.following_facts = list()  # список фактов-следствий


points = list()
lines = list()
angles = list()
segments = list()
polygons = list()
facts = list()
questions = list()


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
                    if convex == 'невыпуклый':
                        polygons.append(Polygon(vertices_class_list, False))
                    else:
                        polygons.append(Polygon(vertices_class_list))
                except IndexError:
                    polygons.append(Polygon(vertices_class_list))

            if len(vertices_list) == 3:
                polygons.append(Polygon(vertices_class_list))

            if len(vertices_list) == 1:
                S = vertices_class_list[0]

                S.specific_properties_point = polygon.split()[1]
                S.specific_properties_triangle = polygon.split()[2]

                A = find_point_with_name(polygon.split()[2][0]).name
                B = find_point_with_name(polygon.split()[2][1]).name
                C = find_point_with_name(polygon.split()[2][2]).name

                AB = find_line_with_points(A, B)
                BC = find_line_with_points(C, B)
                CA = find_line_with_points(A, C)

                if polygon.split()[1] == 'H':
                    find_angle_with_lines(AB, find_line_with_points(C, S.name)).size = 90
                    find_angle_with_lines(find_line_with_points(C, S.name), AB).size = 90
                    find_angle_with_lines(BC, find_line_with_points(A, S.name)).size = 90
                    find_angle_with_lines(find_line_with_points(A, S.name), BC).size = 90
                    find_angle_with_lines(CA, find_line_with_points(B, S.name)).size = 90
                    find_angle_with_lines(find_line_with_points(B, S.name), CA).size = 90

                if polygon.split()[1] == 'O':
                    AS = find_segment_with_points(A, S.name)
                    BS = find_segment_with_points(B, S.name)
                    CS = find_segment_with_points(C, S.name)

                    AS.relations[BS] = Fraction(1)
                    BS.relations[AS] = Fraction(1)
                    AS.relations[CS] = Fraction(1)
                    CS.relations[AS] = Fraction(1)
                    CS.relations[BS] = Fraction(1)
                    BS.relations[CS] = Fraction(1)

                if polygon.split()[1] == 'I':
                    AS = find_line_with_points(A, S.name)
                    BS = find_line_with_points(B, S.name)
                    CS = find_line_with_points(C, S.name)

                    SAC = find_angle_with_lines(AS, CA)
                    BAS = find_angle_with_lines(AB, AS)
                    SBA = find_angle_with_lines(BS, AB)
                    CBS = find_angle_with_lines(BC, BS)
                    SCB = find_angle_with_lines(CS, BC)
                    ACS = find_angle_with_lines(CA, CS)

                    SAC.relations[BAS] = Fraction(1)
                    BAS.relations[SAC] = Fraction(1)
                    SBA.relations[CBS] = Fraction(1)
                    CBS.relations[SBA] = Fraction(1)
                    SCB.relations[ACS] = Fraction(1)
                    ACS.relations[SCB] = Fraction(1)


def segments_create(text):
    if len(text.split()) > 0:
        for segment in text.split(','):
            segment = segment.split()
            try:
                size = float(Fraction(segment[1]))
            except IndexError:
                size = None

            seg = find_segment_with_points(segment[0][0], segment[0][1])
            seg.size = size


def angles_create(text):
    if len(text.split()) > 0:
        for angle in text.split(','):
            angle = angle.split()
            if len(angle) == 2:
                angle_name, angle_size = angle
                A, B, C = list(angle_name)
                if A != B != C != A:
                    A, B, C = check_angle_in_polygon(A, B, C)

                    l1 = find_line_with_points(A, B)
                    l2 = find_line_with_points(B, C)

                    find_angle_with_lines(l1, l2).size = float(Fraction(angle_size))
                    find_angle_with_lines(l2, l1).size = 180 - float(Fraction(angle_size))

            if len(angle) == 3:
                l1, l2, angle_size = angle
                l1 = find_line_with_points(l1[0], l1[1])
                l2 = find_line_with_points(l2[0], l2[1])
                find_angle_with_lines(l1, l2).size = float(Fraction(angle_size))
                find_angle_with_lines(l2, l1).size = 180 - float(Fraction(angle_size))


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
                line.points.add(find_point_with_name(relation.split()[0]))

            if len(relation.split()[1]) == 1:
                seg_1 = find_segment_with_points(relation.split()[1], relation.split()[0][0])
                seg_2 = find_segment_with_points(relation.split()[1], relation.split()[0][1])

                line = find_line_with_points(relation.split()[0][0], relation.split()[0][1])
                line.points.add(find_point_with_name(relation.split()[1]))

            rel = relation.split()[2]
            seg_1.relations[seg_2] = Fraction(rel)
            seg_2.relations[seg_1] = 1 / Fraction(rel)


def angles_relations_create(text):
    if len(text.split()) > 0:
        for relation in text.split(','):
            ang_1, ang_2, rel = relation.split()

            ang_1 = find_angle_with_points(*check_angle_in_polygon(ang_1[0], ang_1[1], ang_1[2]))
            ang_2 = find_angle_with_points(*check_angle_in_polygon(ang_2[0], ang_2[1], ang_2[2]))

            ang_1.relations[ang_2] = Fraction(rel)
            ang_2.relations[ang_1] = 1 / Fraction(rel)


def polygons_relations_create(text):
    if len(text.split()) > 0:
        for relation in text.split(','):
            polygon_1, polygon_2, rel = relation.split()

            for i in range(len(polygon_1)):
                side_1 = find_segment_with_points(polygon_1[i - 1], polygon_1[i])
                side_2 = find_segment_with_points(polygon_2[i - 1], polygon_2[i])

                side_1.relations[side_2] = Fraction(rel)
                side_2.relations[side_1] = 1 / Fraction(rel)

            polygon_1 = find_polygon_with_points(list(polygon_1))
            polygon_2 = find_polygon_with_points(list(polygon_2))

            polygon_1.relations[polygon_2] = Fraction(rel)
            polygon_2.relations[polygon_1] = 1 / Fraction(rel)


def line_intersection_create(text):
    if len(text.split()) > 0:
        for intersection in text.split(','):
            l1, l2, P = intersection.split()

            l1 = find_line_with_segment(find_segment_with_points(l1[0], l1[1]))
            if find_point_with_name(P) not in l1.points:
                l1.points.add(find_point_with_name(P))

            l2 = find_line_with_segment(find_segment_with_points(l2[0], l2[1]))
            if find_point_with_name(P) not in l2.points:
                l2.points.add(find_point_with_name(P))


def questions_create(text):
    if len(text.split()) > 0:
        for question in text.split(','):
            if len(question.split()) == 2:
                if len(question.split()[0]) == 2:
                    seg = find_segment_with_points(question.split()[0][0], question.split()[0][1])
                    questions.append(Fact(len(questions), None, 'size', [seg], None, True))
                if len(question.split()[0]) == 3:
                    ang = find_angle_with_points(check_angle_in_polygon(question.split()[0][0], question.split()[0][1], question.split()[0][2]))
                    questions.append(Fact(len(questions), None, 'size', [ang], None, True))
            if len(question.split()) == 3:
                if len(question.split()[0]) == 2 and len(question.split()[1]) == 2:
                    seg_1 = find_segment_with_points(question.split()[0][0], question.split()[0][1])
                    seg_2 = find_segment_with_points(question.split()[1][0], question.split()[1][1])
                    if question.split()[2] == '?':
                        questions.append(Fact(len(questions), None, 'relation', [seg_1, seg_2], None, True))
                    else:
                        questions.append(Fact(len(questions), None, 'relation', [seg_1, seg_2], Fraction(question.split()[2]), True))
                if question.split()[0][0] != '/' and len(question.split()[0]) == 3 and len(question.split()[1]) == 3:
                    ang_1 = find_angle_with_points(check_angle_in_polygon(question.split()[0][0], question.split()[0][1], question.split()[0][2]))
                    ang_2 = find_angle_with_points(check_angle_in_polygon(question.split()[1][0], question.split()[1][1], question.split()[1][2]))
                    if question.split()[2] == '?':
                        questions.append(Fact(len(questions), None, 'relation', [ang_1, ang_2], None, True))
                    else:
                        questions.append(Fact(len(questions), None, 'relation', [ang_1, ang_2], Fraction(question.split()[2]), True))
                else:
                    polygon_1 = find_polygon_with_points(list(question.split()[0])[1:])
                    polygon_2 = find_polygon_with_points(list(question.split()[1]))
                    if question.split()[2] == '?':
                        questions.append(Fact(len(questions), None, 'relation', [polygon_1, polygon_2], None, True))
                    else:
                        questions.append(Fact(len(questions), None, 'relation', [polygon_1, polygon_2], Fraction(question.split()[2]), True))


# вспомогательная функция для поиска отрезка по вершинам, указываются имена точек
def find_segment_with_points(A, B):
    a = find_point_with_name(A)
    b = find_point_with_name(B)

    for seg in segments:
        if {a, b} == seg.points:
            return seg

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

    new_angle = Angle(l1, l2)
    angles.append(new_angle)
    return new_angle


# вспомогательная функция для поиска многоугольника по его вершинам
def find_polygon_with_points(points):
    for polygon in polygons:
        if set(get_points_names_from_list(polygon.points)) == set(points):
            return polygon

    new_points = list()
    for point in points:
        new_points.append(find_point_with_name(point))
    new_polygon = Polygon(new_points)
    polygons.append(new_polygon)
    return new_polygon


# вспомогательная функция для поиска точки по её имени
def find_point_with_name(A):
    for point in points:
        if A == point.name:
            return point

    new_point = Point(A)
    points.append(new_point)
    return new_point


# вспомогательная функция для получения списка имен точек из списка
def get_points_names_from_list(points_list):
    ret = []
    for point in points_list:
        ret.append(point.name)

    return ret


def check_angle_in_polygon(A, B, C):
    for polygon in polygons:
        for i in range(len(polygon.points)):
            uA, uB, uC = polygon.points[i - 2].name, polygon.points[i - 1].name, polygon.points[i].name

            if uA == A and uB == B and uC == C:
                return C, B, A

            if uA == C and uB == B and uC == A:
                return A, B, C

    return A, B, C


def UseRelations(objects):
    none_count = 0

    for obj in objects:
        if not obj.size:
            none_count += 1

    #if seg_check and none_count == len(objects) != 0:
        #objects[0].size = 3
        #none_count -= 1

    for n in range(none_count):

        for i in range(len(objects)):
            obj_1 = objects[i]

            if not obj_1.size:
                for j in range(len(objects)):
                    obj_2 = objects[j]

                    if obj_2.size:
                        try:
                            obj_1.size = float(obj_2.size / obj_2.relations[obj_1])
                        except Exception:
                            pass


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
    for obj in relations_set:
        if parametr == "angle":
            ret.setdefault(f"object_{angles.index(obj)+len(points)+len(lines)+1}", str(relations_set[obj]))
        if parametr == "segment":
            ret.setdefault(f"object_{segments.index(obj)+len(points)+len(lines)+len(angles)+1}", str(relations_set[obj]))

    return ret


# создание выходной json-ки
def json_create():
    output = dict()
    object_index = 1

    for point in points:
        object = dict()

        object['name'] = point.name
        object['type'] = 'point'
        object['points_on_object'] = None
        object['angle_between_lines'] = None
        object['size'] = None
        object['relations'] = None
        object['convex'] = None

        output[f"object_{object_index}"] = object
        object_index += 1

    for line in lines:
        object = dict()

        object['name'] = None
        object['type'] = 'line'
        object['points_on_object'] = points_processing(line.points)
        object['angle_between_lines'] = None
        object['size'] = None
        object['relations'] = None
        object['convex'] = None

        output[f"object_{object_index}"] = object
        object_index += 1

    for angle in angles:
        object = dict()

        object['name'] = None
        object['type'] = 'angle'
        object['points_on_object'] = None
        object['angle_between_lines'] = lines_processing(angle.lines)
        object['size'] = angle.size
        object['relations'] = relations_processing(angle.relations, 'angle')
        object['convex'] = None

        output[f"object_{object_index}"] = object
        object_index += 1

    for segment in segments:
        object = {}

        object['name'] = None
        object['type'] = 'segment'
        object['points_on_object'] = points_processing(segment.points)
        object['angle_between_lines'] = None
        object['size'] = segment.size
        object['relations'] = relations_processing(segment.relations, 'segment')
        object['convex'] = None

        output[f"object_{object_index}"] = object
        object_index += 1

    for polygon in polygons:
        object = dict()

        object['name'] = None
        object['type'] = 'polygon'
        object['points_on_object'] = points_processing(polygon.points)
        object['angle_between_lines'] = None
        object['size'] = None
        object['relations'] = None
        object['convex'] = polygon.convex

        output[f"object_{object_index}"] = object
        object_index += 1

    return output
