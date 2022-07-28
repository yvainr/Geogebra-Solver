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


class Ray:
    def __init__(self,
                 main_point,
                 points: set):
        self.main_point = main_point
        self.points = points

    def __str__(self):
        return f'main_point: {self.main_point.name}, points: {get_points_names_from_list(self.points)}'


class Angle:
    def __init__(self,
                 ray_one,
                 ray_two,
                 size=None):
        self.rays = [ray_one, ray_two]
        self.size = size
        self.relations = dict()
        self.difference = dict()
        self.addition = dict()
        self.name = f'angle_{len(angles)}'

    def __str__(self):
        str_rays = ''
        str_relations = ''
        str_difference = ''
        str_addition = ''

        for ray in self.rays:
            str_rays += f' {get_points_names_from_list(ray.points)}'

        for rel in self.relations:
            str_relations += f'{get_points_names_from_list(rel.lines[0].points)} {get_points_names_from_list(rel.lines[1].points)} {self.relations[rel]} '

        for dif in self.difference:
            str_difference += f'{get_points_names_from_list(dif.lines[0].points)} {get_points_names_from_list(dif.lines[1].points)} {self.difference[dif]} '

        for add in self.addition:
            str_addition += f'{get_points_names_from_list(add.lines[0].points)} {get_points_names_from_list(add.lines[1].points)} {self.addition[add]} '

        if not str_relations:
            str_relations = 'None '

        if not str_difference:
            str_difference = 'None '

        if not str_addition:
            str_addition = 'None '

        return f'name: {self.name}, rays:{str_rays}, size: {self.size}, relations: {str_relations[:-1]}, difference: {str_difference[:-1]}, addition: {str_addition[:-1]}'


class Segment:
    def __init__(self,
                 point_one,
                 point_two,
                 size=None):
        self.points = {point_one, point_two}
        self.size = size
        self.relations = dict()
        self.difference = dict()
        self.addition = dict()
        self.name = f"segment_{point_one.name}{point_two.name}"

    def __str__(self):
        str_relations = ''
        str_difference = ''
        str_addition = ''

        for rel in self.relations:
            str_relations += f'{get_points_names_from_list(rel.points)}: {self.relations[rel]} '

        for dif in self.difference:
            str_difference += f'{get_points_names_from_list(dif.points)}: {self.difference[dif]} '

        for add in self.addition:
            str_addition += f'{get_points_names_from_list(add.points)}: {self.addition[add]} '

        if not str_relations:
            str_relations = 'None '

        if not str_difference:
            str_difference = 'None '

        if not str_addition:
            str_addition = 'None '

        return f'points: {get_points_names_from_list(self.points)}, size: {self.size}, relations: {str_relations[:-1]}, difference: {str_difference[:-1]}, addition: {str_addition[:-1]}'


class Polygon:
    def __init__(self,
                 vertices,
                 convex=True):
        self.points = vertices
        self.convex = convex
        self.relations = dict()
        self.name = f"polygon_{''.join(get_points_names_from_list(vertices))}"
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
        self.fact_type = fact_type  # relation (отношение), size (значение), difference (вычитание), addition (сложение)
        self.objects = objects
        self.value = value
        self.question = question
        self.description = None
        self.root_facts = set()  # список фактов-причин
        self.following_facts = set()  # список фактов-следствий

    def __str__(self):
        list_root_facts = list()
        list_following_facts = list()
        list_objects = list()

        for root_fact in self.root_facts:
            list_root_facts.append(root_fact)

        for following_fact in self.following_facts:
            list_root_facts.append(following_fact)

        for object in self.objects:
            list_objects.append(object.__str__)

        if not list_root_facts:
            list_root_facts = None

        if not list_following_facts:
            list_following_facts = None

        return f'id: {self.id}, generation: {self.generation}, fact_type: {self.fact_type}, objects: {list_objects}, value: {self.value}, question: {self.question}, description: {self.description}, root_facts: {list_root_facts}, following_facts: {list_following_facts}'

    def show_fact(self):
        draw_data = list()
        mark_color = "#FF1919"

        if len(self.objects) == 2:
            if self.objects[0].__class__.__name__ == 'Segment' and self.objects[1].__class__.__name__ == 'Segment':
                draw_data.append(f'SetVisibleInView({self.objects[0].name}, 1, true)')
                draw_data.append(f'SetVisibleInView({self.objects[1].name}, 1, true)')
                draw_data.append(f'SetColor({self.objects[0].name}, {mark_color})')
                draw_data.append(f'SetColor({self.objects[1].name}, {mark_color})')
            if self.objects[0].__class__.__name__ == 'Angle' and self.objects[1].__class__.__name__ == 'Angle':
                draw_data.append(f'{self.objects[0].name}=Angle(Line({self.objects[0].rays[0].main_point.name}, {list(self.objects[0].rays[0].points)[0].name}), Line({self.objects[0].rays[1].main_point.name}, {list(self.objects[0].rays[1].points)[0].name}))')
                draw_data.append(f'{self.objects[1].name}=Angle(Line({self.objects[1].rays[0].main_point.name}, {list(self.objects[1].rays[0].points)[0].name}), Line({self.objects[1].rays[1].main_point.name}, {list(self.objects[1].rays[1].points)[0].name}))')
            if self.objects[0].__class__.__name__ == 'Polygon' and self.objects[1].__class__.__name__ == 'Polygon':
                draw_data.append(f'SetColor({self.objects[0].name}, {mark_color})')
                draw_data.append(f'SetColor({self.objects[1].name}, {mark_color})')

        if len(self.objects) == 1:
            if self.objects[0].__class__.__name__ == 'Segment':
                draw_data.append(f'SetVisibleInView({self.objects[0].name}, 1, true)')
                draw_data.append(f'SetColor({self.objects[0].name}, {mark_color})')
            if self.objects[0].__class__.__name__ == 'Angle':
                draw_data.append(f'{self.objects[0].name}=Angle(Line({self.objects[0].rays[0].main_point.name}, {list(self.objects[0].rays[0].points)[0].name}), Line({self.objects[0].rays[1].main_point.name}, {list(self.objects[0].rays[1].points)[0].name}))')
            if self.objects[0].__class__.__name__ == 'Polygon':
                draw_data.append(f'SetColor({self.objects[0].name}, {mark_color})')

        return draw_data

    def hide_fact(self):
        draw_data = list()
        standart_color = "#1565C0"

        if len(self.objects) == 2:
            if self.objects[0].__class__.__name__ == 'Segment' and self.objects[1].__class__.__name__ == 'Segment':
                draw_data.append(f'SetVisibleInView({self.objects[0].name}, 1, false)')
                draw_data.append(f'SetVisibleInView({self.objects[1].name}, 1, false)')
                draw_data.append(f'SetColor({self.objects[0].name}, {standart_color})')
                draw_data.append(f'SetColor({self.objects[1].name}, {standart_color})')
            if self.objects[0].__class__.__name__ == 'Angle' and self.objects[1].__class__.__name__ == 'Angle':
                draw_data.append(f'Delete({self.objects[0].name})')
                draw_data.append(f'Delete({self.objects[1].name})')
            if self.objects[0].__class__.__name__ == 'Polygon' and self.objects[1].__class__.__name__ == 'Polygon':
                draw_data.append(f'SetColor({self.objects[0].name}, {standart_color})')
                draw_data.append(f'SetColor({self.objects[1].name}, {standart_color})')

        if len(self.objects) == 1:
            if self.objects[0].__class__.__name__ == 'Segment':
                draw_data.append(f'SetVisibleInView({self.objects[0].name}, 1, false)')
                draw_data.append(f'SetColor({self.objects[0].name}, {standart_color})')
            if self.objects[0].__class__.__name__ == 'Angle':
                draw_data.append(f'Delete({self.objects[0].name})')
            if self.objects[0].__class__.__name__ == 'Polygon':
                draw_data.append(f'SetColor({self.objects[0].name}, {standart_color})')

        return draw_data


points = list()
lines = list()
rays = list()
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
                    if convex == '*':
                        polygons.append(Polygon(vertices_class_list, False))
                    else:
                        polygons.append(Polygon(vertices_class_list))
                except IndexError:
                    polygons.append(Polygon(vertices_class_list))

            if len(vertices_list) == 3:
                polygons.append(Polygon(vertices_class_list))

            # if len(vertices_list) == 1:
            #     S = vertices_class_list[0]
            #
            #     S.specific_properties_point = polygon.split()[1]
            #     S.specific_properties_triangle = polygon.split()[2]
            #
            #     A = find_point_with_name(polygon.split()[2][0]).name
            #     B = find_point_with_name(polygon.split()[2][1]).name
            #     C = find_point_with_name(polygon.split()[2][2]).name
            #
            #     AB = find_line_with_points(A, B)
            #     BC = find_line_with_points(C, B)
            #     CA = find_line_with_points(A, C)
            #
            #     if polygon.split()[1] == 'H':
            #         find_angle_with_lines(AB, find_line_with_points(C, S.name)).size = 90
            #         find_angle_with_lines(find_line_with_points(C, S.name), AB).size = 90
            #         find_angle_with_lines(BC, find_line_with_points(A, S.name)).size = 90
            #         find_angle_with_lines(find_line_with_points(A, S.name), BC).size = 90
            #         find_angle_with_lines(CA, find_line_with_points(B, S.name)).size = 90
            #         find_angle_with_lines(find_line_with_points(B, S.name), CA).size = 90
            #
            #     if polygon.split()[1] == 'O':
            #         AS = find_segment_with_points(A, S.name)
            #         BS = find_segment_with_points(B, S.name)
            #         CS = find_segment_with_points(C, S.name)
            #
            #         AS.relations[BS] = Fraction(1)
            #         BS.relations[AS] = Fraction(1)
            #         AS.relations[CS] = Fraction(1)
            #         CS.relations[AS] = Fraction(1)
            #         CS.relations[BS] = Fraction(1)
            #         BS.relations[CS] = Fraction(1)
            #
            #     if polygon.split()[1] == 'I':
            #         AS = find_line_with_points(A, S.name)
            #         BS = find_line_with_points(B, S.name)
            #         CS = find_line_with_points(C, S.name)
            #
            #         SAC = find_angle_with_lines(AS, CA)
            #         BAS = find_angle_with_lines(AB, AS)
            #         SBA = find_angle_with_lines(BS, AB)
            #         CBS = find_angle_with_lines(BC, BS)
            #         SCB = find_angle_with_lines(CS, BC)
            #         ACS = find_angle_with_lines(CA, CS)
            #
            #         SAC.relations[BAS] = Fraction(1)
            #         BAS.relations[SAC] = Fraction(1)
            #         SBA.relations[CBS] = Fraction(1)
            #         CBS.relations[SBA] = Fraction(1)
            #         SCB.relations[ACS] = Fraction(1)
            #         ACS.relations[SCB] = Fraction(1)


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
            angle_name, angle_size = angle
            A, B, C = list(angle_name)
            if A != B != C != A:
                A, B, C = check_angle_in_polygon(A, B, C)

                find_angle_with_points(A, B, C).size = float(Fraction(angle_size))
                find_angle_with_points(C, B, A).size = 360 - float(Fraction(angle_size))


def segments_relations_create(text):
    if len(text.split()) > 0:
        for relation in text.split(','):
            if len(relation.split()[0]) == len(relation.split()[1]) == 2:
                seg_1 = find_segment_with_points(relation.split()[0][0], relation.split()[0][1])
                seg_2 = find_segment_with_points(relation.split()[1][0], relation.split()[1][1])

                rel = relation.split()[2]
                seg_1.relations[seg_2] = Fraction(rel)
                seg_2.relations[seg_1] = 1 / Fraction(rel)

            if len(relation.split()[0]) == 1:
                seg_1 = find_segment_with_points(relation.split()[0], relation.split()[1][0])
                seg_2 = find_segment_with_points(relation.split()[0], relation.split()[1][1])

                line = find_line_with_points(relation.split()[1][0], relation.split()[1][1])
                line.points.add(find_point_with_name(relation.split()[0]))

                rel = relation.split()[2]
                seg_1.relations[seg_2] = Fraction(rel)
                seg_2.relations[seg_1] = 1 / Fraction(rel)

            if len(relation.split()[1]) == 1:
                seg_1 = find_segment_with_points(relation.split()[1], relation.split()[0][0])
                seg_2 = find_segment_with_points(relation.split()[1], relation.split()[0][1])

                line = find_line_with_points(relation.split()[0][0], relation.split()[0][1])
                line.points.add(find_point_with_name(relation.split()[1]))

                rel = relation.split()[2]
                seg_1.relations[seg_2] = Fraction(rel)
                seg_2.relations[seg_1] = 1 / Fraction(rel)

            if len(relation.split()[0]) == 3 and len(relation.split()[1]) == 2:
                seg_1 = find_segment_with_points(relation.split()[0][0], relation.split()[0][1])
                seg_2 = find_segment_with_points(relation.split()[1][0], relation.split()[1][1])

                if relation.split()[0][2] == '-':
                    dif = relation.split()[2]
                    seg_1.difference[seg_2] = Fraction(dif)
                    seg_2.difference[seg_1] = - Fraction(dif)

                if relation.split()[0][2] == '+':
                    add = relation.split()[2]
                    seg_1.addition[seg_2] = Fraction(add)
                    seg_2.addition[seg_1] = Fraction(add)


def angles_relations_create(text):
    if len(text.split()) > 0:
        for relation in text.split(','):
            ang_1, ang_2, val = relation.split()

            ang_1 = find_angle_with_points(*check_angle_in_polygon(ang_1[0], ang_1[1], ang_1[2]))
            ang_2 = find_angle_with_points(*check_angle_in_polygon(ang_2[0], ang_2[1], ang_2[2]))

            if len(relation.split()[0]) == len(relation.split()[1]) == 3:
                ang_1.relations[ang_2] = Fraction(val)
                ang_2.relations[ang_1] = 1 / Fraction(val)

            if relation.split()[0][3] == '-' and len(relation.split()[0]) == 4 and len(relation.split()[1]) == 3:
                ang_1.difference[ang_2] = Fraction(val)
                ang_2.difference[ang_1] = - Fraction(val)

            if relation.split()[0][3] == '+' and len(relation.split()[0]) == 4 and len(relation.split()[1]) == 3:
                ang_1.addition[ang_2] = Fraction(val)
                ang_2.addition[ang_1] = Fraction(val)


def polygons_relations_create(text):
    if len(text.split()) > 0:
        for relation in text.split(','):
            polygon_1, polygon_2, rel = relation.split()

            for i in range(len(polygon_1)):
                side_1 = find_segment_with_points(polygon_1[i - 1], polygon_1[i])
                side_2 = find_segment_with_points(polygon_2[i - 1], polygon_2[i])

                side_1.relations[side_2] = Fraction(rel)
                side_2.relations[side_1] = 1 / Fraction(rel)

            for i in range(len(polygon_1)):
                ang_1 = find_angle_with_points(polygon_1[i], polygon_1[i - 1], polygon_1[i - 2])
                ang_2 = find_angle_with_points(polygon_2[i], polygon_2[i - 1], polygon_2[i - 2])

                ang_1.relations[ang_2] = Fraction(1)
                ang_2.relations[ang_1] = Fraction(1)

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
                try:
                    val = Fraction(question.split()[1])
                except TypeError:
                    val = None

                if len(question.split()[0]) == 2:
                    seg = find_segment_with_points(question.split()[0][0], question.split()[0][1])
                    questions.append(Fact(len(questions), None, 'size', [seg], val, True))
                if len(question.split()[0]) == 3:
                    ang = find_angle_with_points(*check_angle_in_polygon(question.split()[0][0], question.split()[0][1], question.split()[0][2]))
                    questions.append(Fact(len(questions), None, 'size', [ang], val, True))

            if len(question.split()) == 3:
                if len(question.split()[0]) == 2 and len(question.split()[1]) == 2:
                    seg_1 = find_segment_with_points(question.split()[0][0], question.split()[0][1])
                    seg_2 = find_segment_with_points(question.split()[1][0], question.split()[1][1])

                    if question.split()[2] == '?':
                        questions.append(Fact(len(questions), None, 'relation', [seg_1, seg_2], None, True))
                    else:
                        questions.append(Fact(len(questions), None, 'relation', [seg_1, seg_2], Fraction(question.split()[2]), True))

                elif question.split()[0][0] != '/' and len(question.split()[0]) == 3 and len(question.split()[1]) == 3:
                    ang_1 = find_angle_with_points(*check_angle_in_polygon(question.split()[0][0], question.split()[0][1], question.split()[0][2]))
                    ang_2 = find_angle_with_points(*check_angle_in_polygon(question.split()[1][0], question.split()[1][1], question.split()[1][2]))

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
def find_angle_with_rays(r1, r2):
    for angle in angles:
        if angle.rays == [r1, r2]:
            return angle

    new_angle = Angle(r1, r2)
    angles.append(new_angle)
    return new_angle


def find_ray_with_points(A, B):
    a = find_point_with_name(A)
    b = find_point_with_name(B)

    for ray in rays:
        if a == ray.main_point and {b} <= set(ray.points):
            return ray

    new_ray = Ray(a, {b})
    rays.append(new_ray)
    return new_ray


# вспомогательная функция для поиска угла по точкам
def find_angle_with_points(A, B, C):
    r1 = find_ray_with_points(B, A)
    r2 = find_ray_with_points(B, C)

    for angle in angles:
        if angle.rays == [r1, r2]:
            return angle

    new_angle = Angle(r1, r2)
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


def create_new_data_in_parser(objects):
    none_count = 0

    for obj in objects:
        if not obj.size:
            none_count += 1

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
                            try:
                                obj_1.size = obj_2.size - obj_2.difference[obj_1]
                            except Exception:
                                try:
                                    obj_1.size = obj_2.addition[obj_1] - obj_2.size
                                except Exception:
                                    pass
