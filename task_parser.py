from random import uniform
from objects_types import Objects, Size


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
        self.in_polygon = None

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
                 size=None,
                 name=None):
        self.rays = [ray_one, ray_two]
        self.size = size
        self.relations = dict()
        self.difference = dict()
        self.addition = dict()
        self.name = name

    def __str__(self):
        str_rays = ''
        str_relations = ''
        str_difference = ''
        str_addition = ''

        for ray in self.rays:
            str_rays += f' {[ray.main_point.name] + get_points_names_from_list(ray.points)}'

        for rel in self.relations:
            str_relations += f'{[rel.rays[0].main_point.name] + get_points_names_from_list(rel.rays[0].points)} {[rel.rays[1].main_point.name] + get_points_names_from_list(rel.rays[1].points)} {self.relations[rel]} '

        for dif in self.difference:
            str_difference += f'{get_points_names_from_list(dif.rays[0].points)} {get_points_names_from_list(dif.rays[1].points)} {self.difference[dif]} '

        for add in self.addition:
            str_addition += f'{get_points_names_from_list(add.rays[0].points)} {get_points_names_from_list(add.rays[1].points)} {self.addition[add]} '

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

        return f'name: {self.name}, size: {self.size}, relations: {str_relations[:-1]}, difference: {str_difference[:-1]}, addition: {str_addition[:-1]}'


class Polygon:
    def __init__(self,
                 vertices,
                 convex=True):
        self.points = vertices
        self.convex = convex
        self.relations = dict()
        self.name = f"polygon_{''.join(get_points_names_from_list(vertices))}"

    def __str__(self):
        return f'name: {self.name}, convex: {self.convex}'


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
            list_objects.append(object.__str__())

        if not list_root_facts:
            list_root_facts = None

        if not list_following_facts:
            list_following_facts = None

        return f'id: {self.id}, generation: {self.generation}, fact_type: {self.fact_type}, objects: {list_objects}, value: {self.value}, question: {self.question}, description: {self.description}, root_facts: {list_root_facts}, following_facts: {list_following_facts}'

    def show_fact(self):
        draw_data = list()
        mark_color = "#FF1919"

        for obj in self.objects:
            if obj.__class__.__name__ == 'Segment':
                draw_data.append(f'SetVisibleInView({obj.name}, 1, true)')
                draw_data.append(f'SetColor({obj.name}, "{mark_color}")')
            if obj.__class__.__name__ == 'Angle':
                draw_data.append(f'{obj.name}=Angle(Line({obj.rays[0].main_point.name}, {list(obj.rays[0].points)[0].name}), Line({obj.rays[1].main_point.name}, {list(obj.rays[1].points)[0].name}))')
            if obj.__class__.__name__ == 'Polygon':
                draw_data.append(f'SetColor({obj.name}, "{mark_color}")')

        if self.fact_type == 'relation' and self.objects[0].__class__.__name__ == 'Polygon' and self.value:
            try:
                rel1, rel2 = str(self.value).split('/')
            except ValueError:
                rel1, rel2 = self.value, 1
            x_points_1, y_points_1, x_points_2, y_points_2 = str(), str(), str(), str()

            for point in self.objects[0].points:
                x_points_1 += f'x({point.name})+'
                y_points_1 += f'y({point.name})+'

            for point in self.objects[1].points:
                x_points_2 += f'x({point.name})+'
                y_points_2 += f'y({point.name})+'

            draw_data.append(
                f'text1=Text("{rel1}X", (({x_points_1[:-1]})/{len(self.objects[0].points)}, ({y_points_1[:-1]})/{len(self.objects[0].points)}), false, true)')
            draw_data.append(
                f'text2=Text("{rel2}X", (({x_points_2[:-1]})/{len(self.objects[1].points)}, ({y_points_2[:-1]})/{len(self.objects[1].points)}), false, true)')

        elif self.fact_type == 'relation' and self.objects[0].__class__.__name__ == 'Segment' and self.value:
            A, B = self.objects[0].points
            C, D = self.objects[1].points
            try:
                rel1, rel2 = str(self.value).split('/')
            except ValueError:
                rel1, rel2 = self.value, 1
            draw_data.append(
                f'text1=Text("{rel1}X", ((x({A.name}) + x({B.name})) / 2, ((y({A.name}) + y({B.name})) / 2) + 0.75), false, true)')
            draw_data.append(
                f'text2=Text("{rel2}X", ((x({C.name}) + x({D.name})) / 2, ((y({C.name}) + y({D.name})) / 2) + 0.75), false, true)')

        elif self.fact_type == 'size' and self.objects[0].__class__.__name__ == 'Segment' and self.value:
            A, B = self.objects[0].points
            draw_data.append(
                f'text=Text({self.value}, ((x({A.name}) + x({B.name})) / 2, ((y({A.name}) + y({B.name})) / 2) + 0.75), true, true)')

        return draw_data

    def hide_fact(self):
        draw_data = list()
        standart_color = "#1565C0"

        for obj in self.objects:
            if obj.__class__.__name__ == 'Segment':
                draw_data.append(f'SetVisibleInView({obj.name}, 1, false)')
                draw_data.append(f'SetColor({obj.name}, "{standart_color}")')
            if obj.__class__.__name__ == 'Angle':
                draw_data.append(f'Delete({obj.name})')
            if obj.__class__.__name__ == 'Polygon':
                draw_data.append(f'SetColor({obj.name}, "{standart_color}")')

        if self.fact_type == 'relation' and self.value and (self.objects[0].__class__.__name__ == 'Segment' or self.objects[0].__class__.__name__ == 'Polygon'):
            draw_data.append(f'Delete(text1)')
            draw_data.append(f'Delete(text2)')

        if self.fact_type == 'size' and self.objects[0].__class__.__name__ == 'Segment' and self.value:
            draw_data.append(f'Delete(text)')

        return draw_data


task_data = Objects()
# drawer_data = Objects()
solver_data = Objects()


def polygons_create(text):
    if len(text.split()) > 0:
        for data in [task_data, solver_data]:
            for polygon in text.split(','):
                vertices_list = list(polygon.split()[0])
                vertices_class_list = list()

                for vertice in vertices_list:
                    vertices_class_list.append(find_point_with_name(vertice, data))

                if len(vertices_list) > 1:
                    for vertice_index in range(len(vertices_list)):
                        find_segment_with_points(vertices_list[vertice_index-1], vertices_list[vertice_index], data)

                if len(vertices_list) > 3:
                    try:
                        convex = polygon.split()[1]
                        if convex == '*':
                            data.polygons.append(Polygon(vertices_class_list, False))
                        else:
                            data.polygons.append(Polygon(vertices_class_list))
                    except IndexError:
                        data.polygons.append(Polygon(vertices_class_list))

                if len(vertices_list) == 3:
                    data.polygons.append(Polygon(vertices_class_list))
                
                # точка внутри многоугольника
                # if len(vertices_list) == 1:
                #     if polygon.split()[1] == 'in':
                #         vertices_class_list[0].in_polygon = find_polygon_with_points(polygon.split()[2], data)

                # замечательные точки
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
                #         AS.relations[BS] = Size(1)
                #         BS.relations[AS] = Size(1)
                #         AS.relations[CS] = Size(1)
                #         CS.relations[AS] = Size(1)
                #         CS.relations[BS] = Size(1)
                #         BS.relations[CS] = Size(1)
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
                #         SAC.relations[BAS] = Size(1)
                #         BAS.relations[SAC] = Size(1)
                #         SBA.relations[CBS] = Size(1)
                #         CBS.relations[SBA] = Size(1)
                #         SCB.relations[ACS] = Size(1)
                #         ACS.relations[SCB] = Size(1)


def segments_create(text):
    if len(text.split()) > 0:
        for data in [task_data, solver_data]:
            for segment in text.split(','):
                segment = segment.split()
                try:
                    size = Size(segment[1])
                except IndexError:
                    size = None

                seg = find_segment_with_points(segment[0][0], segment[0][1], data)
                seg.size = size


def angles_create(text):
    if len(text.split()) > 0:
        for data in [task_data, solver_data]:
            for angle in text.split(','):
                angle = angle.split()
                angle_name, angle_size = angle
                A, B, C = list(angle_name)
                if A != B != C != A:
                    find_angle_with_points(A, B, C, data, True).size = Size(angle_size)
                    # find_angle_with_points(C, B, A, data).size = Size(360) - Size(angle_size)


def segments_relations_create(text):
    if len(text.split()) > 0:
        for data in [task_data, solver_data]:
            for relation in text.split(','):
                if len(relation.split()[0]) == len(relation.split()[1]) == 2:
                    seg_1 = find_segment_with_points(relation.split()[0][0], relation.split()[0][1], data)
                    seg_2 = find_segment_with_points(relation.split()[1][0], relation.split()[1][1], data)

                    rel = relation.split()[2]
                    seg_1.relations[seg_2] = Size(rel)
                    seg_2.relations[seg_1] = 1 / Size(rel)

                if len(relation.split()[0]) == 1:
                    seg_1 = find_segment_with_points(relation.split()[0], relation.split()[1][0], data)
                    seg_2 = find_segment_with_points(relation.split()[0], relation.split()[1][1], data)

                    line = find_line_with_points(relation.split()[1][0], relation.split()[1][1], data)
                    line.points.add(find_point_with_name(relation.split()[0], data))

                    rel = relation.split()[2]
                    seg_1.relations[seg_2] = Size(rel)
                    seg_2.relations[seg_1] = 1 / Size(rel)

                if len(relation.split()[1]) == 1:
                    seg_1 = find_segment_with_points(relation.split()[1], relation.split()[0][0], data)
                    seg_2 = find_segment_with_points(relation.split()[1], relation.split()[0][1], data)

                    line = find_line_with_points(relation.split()[0][0], relation.split()[0][1], data)
                    line.points.add(find_point_with_name(relation.split()[1], data))

                    rel = relation.split()[2]
                    seg_1.relations[seg_2] = Size(rel)
                    seg_2.relations[seg_1] = 1 / Size(rel)

                if len(relation.split()[0]) == 3 and len(relation.split()[1]) == 2:
                    seg_1 = find_segment_with_points(relation.split()[0][0], relation.split()[0][1], data)
                    seg_2 = find_segment_with_points(relation.split()[1][0], relation.split()[1][1], data)

                    if relation.split()[0][2] == '-':
                        dif = relation.split()[2]
                        seg_1.difference[seg_2] = Size(dif)
                        seg_2.difference[seg_1] = - Size(dif)

                    if relation.split()[0][2] == '+':
                        add = relation.split()[2]
                        seg_1.addition[seg_2] = Size(add)
                        seg_2.addition[seg_1] = Size(add)


def angles_relations_create(text):
    if len(text.split()) > 0:
        for data in [task_data, solver_data]:
            for relation in text.split(','):
                ang_1, ang_2, val = relation.split()

                ang_1 = find_angle_with_points(ang_1[0], ang_1[1], ang_1[2], data, True)
                ang_2 = find_angle_with_points(ang_2[0], ang_2[1], ang_2[2], data, True)

                if len(relation.split()[0]) == len(relation.split()[1]) == 3:
                    ang_1.relations[ang_2] = Size(val)
                    ang_2.relations[ang_1] = 1 / Size(val)

                elif relation.split()[0][3] == '-' and len(relation.split()[0]) == 4 and len(relation.split()[1]) == 3:
                    ang_1.difference[ang_2] = Size(val)
                    ang_2.difference[ang_1] = - Size(val)

                elif relation.split()[0][3] == '+' and len(relation.split()[0]) == 4 and len(relation.split()[1]) == 3:
                    ang_1.addition[ang_2] = Size(val)
                    ang_2.addition[ang_1] = Size(val)


def polygons_relations_create(text):
    if len(text.split()) > 0:
        for data in [task_data, solver_data]:
            for relation in text.split(','):
                polygon_1, polygon_2, rel = relation.split()

                for i in range(len(polygon_1)):
                    side_1 = find_segment_with_points(polygon_1[i - 1], polygon_1[i], data)
                    side_2 = find_segment_with_points(polygon_2[i - 1], polygon_2[i], data)

                    side_1.relations[side_2] = Size(rel)
                    side_2.relations[side_1] = 1 / Size(rel)

                for i in range(len(polygon_1)):
                    ang_1 = find_angle_with_points(polygon_1[i], polygon_1[i - 1], polygon_1[i - 2], data)
                    ang_2 = find_angle_with_points(polygon_2[i], polygon_2[i - 1], polygon_2[i - 2], data)

                    ang_1.relations[ang_2] = Size(1)
                    ang_2.relations[ang_1] = Size(1)

                polygon_1 = find_polygon_with_points(list(polygon_1), data)
                polygon_2 = find_polygon_with_points(list(polygon_2), data)

                polygon_1.relations[polygon_2] = Size(rel)
                polygon_2.relations[polygon_1] = 1 / Size(rel)


def line_intersection_create(text):
    if len(text.split()) > 0:
        for data in [task_data, solver_data]:
            for intersection in text.split(','):
                l1, l2, P = intersection.split()

                l1 = find_line_with_segment(find_segment_with_points(l1[0], l1[1], data), data)
                if find_point_with_name(P, data) not in l1.points:
                    l1.points.add(find_point_with_name(P, data))

                l2 = find_line_with_segment(find_segment_with_points(l2[0], l2[1], data), data)
                if find_point_with_name(P, data) not in l2.points:
                    l2.points.add(find_point_with_name(P, data))


def questions_create(text):
    if len(text.split()) > 0:
        for data in [task_data, solver_data]:
            for question in text.split(','):
                if len(question.split()) == 2:
                    try:
                        val = Size(question.split()[1])
                    except ValueError:
                        val = None

                    if len(question.split()[0]) == 2:
                        seg = find_segment_with_points(question.split()[0][0], question.split()[0][1], data)
                        data.questions.append(Fact(len(data.questions), None, 'size', [seg], val, True))
                    if len(question.split()[0]) == 3:
                        ang = find_angle_with_points(question.split()[0][0], question.split()[0][1], question.split()[0][2], data, True)
                        data.questions.append(Fact(len(data.questions), None, 'size', [ang], val, True))

                if len(question.split()) == 3:
                    if len(question.split()[0]) == 2 and len(question.split()[1]) == 2:
                        seg_1 = find_segment_with_points(question.split()[0][0], question.split()[0][1], data)
                        seg_2 = find_segment_with_points(question.split()[1][0], question.split()[1][1], data)

                        if question.split()[2] == '?':
                            data.questions.append(Fact(len(data.questions), None, 'relation', [seg_1, seg_2], None, True))
                        else:
                            data.questions.append(Fact(len(data.questions), None, 'relation', [seg_1, seg_2], Size(question.split()[2]), True))

                    elif question.split()[0][0] != '/' and len(question.split()[0]) == 3 and len(question.split()[1]) == 3:
                        ang_1 = find_angle_with_points(question.split()[0][0], question.split()[0][1], question.split()[0][2], data, True)
                        ang_2 = find_angle_with_points(question.split()[1][0], question.split()[1][1], question.split()[1][2], data, True)

                        if question.split()[2] == '?':
                            data.questions.append(Fact(len(data.questions), None, 'relation', [ang_1, ang_2], None, True))
                        else:
                            data.questions.append(Fact(len(data.questions), None, 'relation', [ang_1, ang_2], Size(question.split()[2]), True))

                    else:
                        polygon_1 = find_polygon_with_points(list(question.split()[0])[1:], data)
                        polygon_2 = find_polygon_with_points(list(question.split()[1]), data)

                        if question.split()[2] == '?':
                            data.questions.append(Fact(len(data.questions), None, 'relation', [polygon_1, polygon_2], None, True))
                        else:
                            data.questions.append(Fact(len(data.questions), None, 'relation', [polygon_1, polygon_2], Size(question.split()[2]), True))


# вспомогательная функция для поиска отрезка по вершинам, указываются имена точек
def find_segment_with_points(A, B, data=None):
    if not data:
        data = solver_data

    a = find_point_with_name(A, data)
    b = find_point_with_name(B, data)

    for seg in data.segments:
        if {a, b} == seg.points:
            return seg

    new_segment = Segment(a, b)
    data.segments.append(new_segment)
    return new_segment


# вспомогательная функция для поиска прямой по точкам на ней, указываются имена точек
def find_line_with_points(A, B, data=None):
    if not data:
        data = solver_data

    a = find_point_with_name(A, data)
    b = find_point_with_name(B, data)

    for line in data.lines:
        if {a, b} <= set(line.points):
            return line

    new_line = Line({a, b})
    data.lines.append(new_line)
    return new_line


# вспомогательная функция для поиска прямой по отрезку на ней
def find_line_with_segment(seg, data=None):
    if not data:
        data = solver_data

    A, B = seg.points
    return find_line_with_points(A.name, B.name, data)


# вспомогательная функция для поиска угла по прямым, его задающим
def find_angle_with_rays(r1, r2, data=None):
    if not data:
        data = solver_data

    for angle in data.angles:
        if angle.rays == [r1, r2]:
            return angle

    new_angle = Angle(r1, r2, None, f'angle_{len(data.angles)}')
    data.angles.append(new_angle)
    return new_angle


def find_ray_with_points(A, B, data=None):
    if not data:
        data = solver_data

    a = find_point_with_name(A, data)
    b = find_point_with_name(B, data)

    for ray in data.rays:
        if a == ray.main_point and {b} <= set(ray.points):
            return ray

    new_ray = Ray(a, {b})
    data.rays.append(new_ray)
    return new_ray


# вспомогательная функция для поиска угла по точкам
def find_angle_with_points(A, B, C, data=None, check_in_triangle=False):
    if not data:
        data = solver_data

    if check_in_triangle:
        A, B, C = check_angle_in_polygon(A, B, C, data)

    r1 = find_ray_with_points(B, A, data)
    r2 = find_ray_with_points(B, C, data)

    for angle in data.angles:
        if angle.rays == [r1, r2]:
            return angle

    new_angle = Angle(r1, r2, None, f'angle_{len(data.angles)}')
    data.angles.append(new_angle)
    return new_angle


# вспомогательная функция для поиска многоугольника по его вершинам
def find_polygon_with_points(points, data=None):
    if not data:
        data = solver_data

    for polygon in data.polygons:
        polygon_points_names = get_points_names_from_list(polygon.points)
        if len(polygon_points_names) == len(points):
            # if len(points) == 3:
            #     if set(polygon_points_names) == set(points):
            #         return polygon
            # else:
            for i in range(len(points)):
                if (points[i:] + points[:i]) == polygon_points_names:
                    return polygon

    new_points = list()
    for point in points:
        new_points.append(find_point_with_name(point))
    new_polygon = Polygon(new_points)
    data.polygons.append(new_polygon)
    return new_polygon


# вспомогательная функция для поиска точки по её имени
def find_point_with_name(A, data=None):
    if not data:
        data = solver_data

    for point in data.points:
        if A == point.name:
            return point

    new_point = Point(A)
    data.points.append(new_point)
    return new_point


# вспомогательная функция для получения списка имен точек из списка
def get_points_names_from_list(points_list):
    ret = []
    for point in points_list:
        ret.append(point.name)

    return ret


def check_angle_in_polygon(A, B, C, data=None):
    if not data:
        data = solver_data

    for polygon in data.polygons:
        for i in range(len(polygon.points)):
            uA, uB, uC = polygon.points[i - 2].name, polygon.points[i - 1].name, polygon.points[i].name

            if uA == A and uB == B and uC == C:
                return C, B, A

            if uA == C and uB == B and uC == A:
                return A, B, C

    return A, B, C
