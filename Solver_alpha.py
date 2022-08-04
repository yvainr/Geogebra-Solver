from fractions import Fraction
import task_parser as tp

Proportion_theorem = True
Cos_theorem_allowed = True
Sin_theorem_allowed = True

# Индекс последнего добавленного факта
ind = 0
ir = 0
facts_indexes = []


def rays_on_same_line(ray1, ray2):
    if tp.find_line_with_points(ray1.main_point.name, list(ray1.points)[0].name, tp.solver_data) == tp.find_line_with_points(ray2.main_point.name, list(ray2.points)[0].name, tp.solver_data):
        return True
    else:
        return False


def angle_between_rays(ray1, ray2):
    if (set([ray1.main_point]) | ray1.points) & (set([ray2.main_point]) | ray2.points) == set():
        return 180
    elif ray1.main_point in ray2.points and ray2.main_point in ray1.points:
        return 180
    elif ray1.main_point == ray2.main_point and (set([ray1.main_point])) & (set([ray2.main_point])):
        return 180
    else:
        return 0

def pre_work():
    global ind, segments2, angles2
    # Добавляет факты с отрезками и углами
    for i, ang in enumerate(tp.solver_data.angles):
        if ang.size:
            update_facts([ang], ang.size, {}, "size")
            angles2[i] = ind
        else:
            angles2[i] = -1

    for i, seg in enumerate(tp.solver_data.segments):
        if seg.size:
            update_facts([seg], seg.size, {}, "size")
            segments2[i] = ind
        else:
            segments2[i] = -1

# Неприятная функция, добавляющая все возможные прямые, отрезки, треугольники и углы
def first():
    global ind, segments2, angles2
    # Перебирает тройки и двойки точек, проверяет существует ли прямая (отрезок) с данными двумя точками, существует ли треугольник с этими тремя точками
    for p1 in tp.solver_data.points:
        for p2 in tp.solver_data.points:
            if p1 != p2:
                for p3 in tp.solver_data.points:
                    if p3 != p1 and p3 != p2:
                        tp.find_polygon_with_points([p1.name, p2.name, p3.name], tp.solver_data)


                tp.find_line_with_points(p1.name, p2.name, tp.solver_data)

                now_len_seg = len(tp.solver_data.segments)

                seg = tp.find_segment_with_points(p1.name, p2.name, tp.solver_data)

                if now_len_seg != len(tp.solver_data.segments):
                    segments2 = segments2 + [-1]

                tp.find_ray_with_points(p1.name, p2.name, tp.solver_data)


    for i1, ray1 in enumerate(tp.solver_data.rays):
        for i2, ray2 in enumerate(tp.solver_data.rays):
            if i1 > i2:
                now_len_ang = len(tp.solver_data.angles)

                ang1 = tp.find_angle_with_rays(ray1, ray2, tp.solver_data)
                ang2 = tp.find_angle_with_rays(ray2, ray1, tp.solver_data)

                if rays_on_same_line(ray1, ray2):
                    ang1.size = angle_between_rays(ray1, ray2)
                    update_facts([ang1], ang1.size, {}, "size")
                    angles2 = angles2 + [ind]

                    ang2.size = angle_between_rays(ray1, ray2)
                    update_facts([ang2], ang2.size, {}, "size")
                    angles2 = angles2 + [ind]
                else:
                    if len(tp.solver_data.angles) - now_len_ang == 1:
                        angles2 = angles2 + [-1]
                    elif len(tp.solver_data.angles) - now_len_ang == 2:
                        angles2 = angles2 + [-1, -1]

                update_facts([ang1, ang2], 360, {}, "addition")


def add_relations_later():
    global segments2, angles2
    if isinstance(tp.solver_data.facts[-1].objects[0], tp.Segment):
        for i1, seg1 in enumerate(tp.solver_data.segments):
            seg2 = tp.solver_data.facts[-1].objects[0]
            if seg1.size and seg2.size and seg1 != seg2:
                in1 = segments2[i1]
                in2 = tp.solver_data.facts[-1].id
                if in1 != -1:
                    update_facts([seg1, seg2], seg1.size / seg2.size, {in1, in2}, "relation")
                    update_facts([seg2, seg1], seg2.size / seg1.size, {in1, in2}, "relation")

    if isinstance(tp.solver_data.facts[-1].objects[0], tp.Angle):
        for i1, ang1 in enumerate(tp.solver_data.angles):
            ang2 = tp.solver_data.facts[-1].objects[0]
            if ang1.size and ang2.size and ang1 != ang2:
                in1 = angles2[i1]
                in2 = tp.solver_data.facts[-1].id
                if in1 != -1:
                    update_facts([ang1, ang2], ang1.size / ang2.size, {in1, in2}, "relation")
                    update_facts([ang2, ang1], ang2.size / ang1.size, {in1, in2}, "relation")



# Находит факт по объектам в нём (если strict - то конкретно с этими объектами, иначе он находит факт где мы находим значение этого объекта)
def find_in_facts_with_obj(obj, not_strict, extra_type, extra_value):
    if not not_strict:
        for x in tp.solver_data.facts:
            if set(x.objects) == set(obj):
                return x.id

    elif not_strict == "extra":
        for x in tp.solver_data.facts:
            if x.objects == obj and x.fact_type == extra_type:
                return x.id

    elif not_strict == "half_hard":
        for x in tp.solver_data.facts:
            if set(x.objects) == set(obj) and extra_type == x.fact_type:
                if extra_value:
                    if x.value:
                        return x.id
                else:
                    if not x.value:
                        return x.id


# Обновляет факты
def update_facts(fact_obj, value, roofs, reason):
    global ind
    tp.solver_data.facts.append(tp.Fact(ind, -1, reason, fact_obj, value))
    for roof in roofs:
        tp.solver_data.facts[roof].following_facts.add(ind)
        tp.solver_data.facts[-1].root_facts.add(roof)
    ind += 1
    if reason == "size":
        add_relations_later()
        add_size_fact()


# Обсчитывает вертикальные углы
def fix_all_angles():
    global ind
    for ray1 in tp.solver_data.rays:
        for ray2 in tp.solver_data.rays:
            if ray1 != ray2:
                for ray3 in tp.solver_data.rays:
                    if ray3 != ray1 and ray3 != ray2:

                        ang1 = tp.find_angle_with_rays(ray1, ray2, tp.solver_data)
                        ang2 = tp.find_angle_with_rays(ray2, ray3, tp.solver_data)
                        ang = tp.find_angle_with_rays(ray1, ray3, tp.solver_data)

                        update_facts([ang, ang1, ang2], [], {}, "addition")


# Выдает все данные об этом треугольнике
def search_triangle(triangle):
    global ind
    A, B, C = triangle.points[0], triangle.points[1], triangle.points[2]

    AB = tp.find_segment_with_points(A.name, B.name, tp.solver_data)
    BC = tp.find_segment_with_points(B.name, C.name, tp.solver_data)
    CA = tp.find_segment_with_points(C.name, A.name, tp.solver_data)

    ABC = tp.find_angle_with_points(C.name, B.name, A.name, tp.solver_data)
    CAB = tp.find_angle_with_points(B.name, A.name, C.name, tp.solver_data)
    BCA = tp.find_angle_with_points(A.name, C.name, B.name, tp.solver_data)

    return [C, B, A, AB, CA, BC, BCA, ABC, CAB]


# Корректирует равенства сторон и углов в равнобедренном треугольнике
def correct_size(ABC, BCA, CA, AB):
    global ind

    if find_in_facts_with_obj([ABC, BCA], "extra", "relation", None):
        if tp.solver_data.facts[find_in_facts_with_obj([ABC, BCA], "extra", "relation", None)].value == 1:
            if not find_in_facts_with_obj([AB, CA], "extra", "relation", None):
                update_facts([AB, CA], 1, {find_in_facts_with_obj([ABC, BCA], "extra", "relation", None)}, "relation")
                update_facts([CA, AB], 1, {find_in_facts_with_obj([ABC, BCA], "extra", "relation", None)}, "relation")

                if CA.size and not AB.size:
                    AB.size = CA.size

                elif AB.size and not CA.size:
                    CA.size = AB.size

    if find_in_facts_with_obj([AB, CA], "extra", "relation", None):
        if tp.solver_data.facts[find_in_facts_with_obj([AB, CA], "extra", "relation", None)].value == 1:
            if not find_in_facts_with_obj([ABC, BCA], "extra", "relation", None):
                update_facts([ABC, BCA], 1, {find_in_facts_with_obj([AB, CA], "extra", "relation", None)}, "relation")
                update_facts([BCA, ABC], 1, {find_in_facts_with_obj([AB, CA], "extra", "relation", None)}, "relation")

                if BCA.size and not ABC.size:
                    BCA.size = ABC.size
                elif ABC.size and not BCA.size:
                    ABC.size = BCA.size


# Проверяет равенство величин объектов, при их не None_овости
def equal(AB, BC):
    if AB.size == BC.size and AB.size:
        return True
    else:
        return False


# Делает углы, где один из них None, а другой - нет, равными (из подобия треугольников)
def equal_them(A, B, fact):
    update_facts([B, A], 1, {fact}, "relation")
    update_facts([A, B], 1, {fact}, "relation")

    if A.size and not B.size:
        B.size = Fraction(A.size)

    if B.size and not A.size:
        A.size = Fraction(B.size)


# It makes Делает стороны, где один из них None, а другой - нет, подобными (из подобия треугольников)
def simil_them(AB, A1B1, k, fact):
    update_facts([A1B1, AB], 1 / k, {fact}, "relation")
    update_facts([AB, A1B1], k, {fact}, "relation")

    if AB.size and not A1B1.size:
        A1B1.size = Fraction(AB.size / k)

    if A1B1.size and not AB.size:
        AB.size = Fraction(A1B1.size * k)


# Находит все стороны и углы, которые может из равнобедренности, во всех р/б треугольниках
def isosceles_triangles():
    for triangle in tp.solver_data.polygons:
        if len(triangle.points) == 3:
            [A, B, C, AB, BC, CA, BCA, CAB, ABC] = search_triangle(triangle)
            correct_size(ABC, BCA, CA, AB)
            correct_size(ABC, CAB, CA, BC)
            correct_size(CAB, BCA, BC, AB)


# Возвращает отношение двух объектов, если это нужно (когда они оба не None)
def similarity_if_not_None(AB, BC):
    if AB.size and BC.size:
        return AB.size / BC.size
    else:
        return None


# Добавляет новые факты следующие из подобия треугольников
def consequences_of_similarity(AB, A1B1, BC, B1C1, CA, C1A1, BCA, B1C1A1, CAB, C1A1B1, ABC, A1B1C1, k):
    fact = ind
    simil_them(AB, A1B1, k, fact)
    simil_them(BC, B1C1, k, fact)
    simil_them(CA, C1A1, k, fact)
    equal_them(BCA, B1C1A1, fact)
    equal_them(CAB, C1A1B1, fact)
    equal_them(ABC, A1B1C1, fact)


# Проверяет все возможные варианты подобия трекугольников, если вершины для подобия указаны в правильном порядке
def similaritys_triangles(triangle1, triangle2,AB, CA, BC, BCA, ABC, CAB, A1B1, C1A1, B1C1, B1C1A1, A1B1C1, C1A1B1):
    if not find_in_facts_with_obj([triangle1, triangle2], "extra", "relation", None):

        # print(AB.size, BC.size, CA.size, BCA.size, CAB.size, ABC.size, A1B1.size, B1C1.size, C1A1.size, B1C1A1.size, C1A1B1.size, A1B1C1.size)
        # print(beautiful_object(AB), beautiful_object(BC), beautiful_object(CA), beautiful_object(BCA), beautiful_object(CAB), beautiful_object(ABC), beautiful_object(A1B1), beautiful_object(B1C1), beautiful_object(C1A1), beautiful_object(B1C1A1), beautiful_object(C1A1B1), beautiful_object(A1B1C1))

        k = similarity_if_not_None(AB, A1B1)
        if not k:
            k = similarity_if_not_None(BC, B1C1)
            if not k:
                k = similarity_if_not_None(CA, C1A1)

        if k:
            if (similarity_if_not_None(AB, A1B1) == similarity_if_not_None(BC, B1C1) and equal(ABC, A1B1C1) and similarity_if_not_None(AB, A1B1)):


                roots = {find_in_facts_with_obj([AB, A1B1], "extra", "relation", None), find_in_facts_with_obj([ABC, A1B1C1], "extra", "relation", None),
                         find_in_facts_with_obj([BC, B1C1], "extra", "relation", None)}

                update_facts([triangle1, triangle2], k, roots, "relation")
                update_facts([triangle2, triangle1], 1 / k, roots, "relation")

                consequences_of_similarity(AB, A1B1, BC, B1C1, CA, C1A1, BCA, B1C1A1, CAB, C1A1B1, ABC, A1B1C1, k)

            elif (similarity_if_not_None(AB, A1B1) == similarity_if_not_None(CA, C1A1) and equal(CAB,
                                                                                             C1A1B1) and similarity_if_not_None(
                AB, A1B1)):

                roots = {find_in_facts_with_obj([CAB, C1A1B1], "extra", "relation", None), find_in_facts_with_obj([AB, A1B1], "extra", "relation", None),
                         find_in_facts_with_obj([CA, C1A1], "extra", "relation", None)}

                update_facts([triangle1, triangle2], k, roots, "relation")
                update_facts([triangle2, triangle1], 1 / k, roots, "relation")

                consequences_of_similarity(AB, A1B1, BC, B1C1, CA, C1A1, BCA, B1C1A1, CAB, C1A1B1, ABC, A1B1C1, k)

            elif (similarity_if_not_None(BC, B1C1) == similarity_if_not_None(CA, C1A1) and equal(BCA,
                                                                                             B1C1A1) and similarity_if_not_None(
                BC, B1C1)):

                roots = {find_in_facts_with_obj([BC, B1C1], "extra", "relation", None), find_in_facts_with_obj([BCA, B1C1A1], "extra", "relation", None),
                         find_in_facts_with_obj([CA, C1A1], "extra", "relation", None)}

                update_facts([triangle1, triangle2], k, roots, "relation")
                update_facts([triangle2, triangle1], 1 / k, roots, "relation")

                consequences_of_similarity(AB, A1B1, BC, B1C1, CA, C1A1, BCA, B1C1A1, CAB, C1A1B1, ABC, A1B1C1, k)

            elif (equal(ABC, A1B1C1) and equal(CAB, C1A1B1) and similarity_if_not_None(AB, A1B1)):

                roots = {find_in_facts_with_obj([ABC, A1B1C1], "extra", "relation", None), find_in_facts_with_obj([CAB, C1A1B1], "extra", "relation", None),
                         find_in_facts_with_obj([AB, A1B1], "extra", "relation", None)}

                update_facts([triangle1, triangle2], k, roots, "relation")
                update_facts([triangle2, triangle1], 1 / k, roots, "relation")

                consequences_of_similarity(AB, A1B1, BC, B1C1, CA, C1A1, BCA, B1C1A1, CAB, C1A1B1, ABC, A1B1C1, k)

            elif (equal(ABC, A1B1C1) and equal(BCA, B1C1A1) and similarity_if_not_None(BC, B1C1)):

                roots = {find_in_facts_with_obj([ABC, A1B1C1], "extra", "relation", None), find_in_facts_with_obj([BCA, B1C1A1], "extra", "relation", None),
                         find_in_facts_with_obj([BC, B1C1], "extra", "relation", None)}

                update_facts([triangle1, triangle2], k, roots, "relation")
                update_facts([triangle2, triangle1], 1 / k, roots, "relation")

                consequences_of_similarity(AB, A1B1, BC, B1C1, CA, C1A1, BCA, B1C1A1, CAB, C1A1B1, ABC, A1B1C1, k)

            elif (similarity_if_not_None(CA, C1A1) == similarity_if_not_None(AB, A1B1) and similarity_if_not_None(BC,
                                                                                                                  B1C1) == similarity_if_not_None(
                    AB, A1B1) and similarity_if_not_None(AB, A1B1)):

                roots = {find_in_facts_with_obj([AB, A1B1], "extra", "relation", None), find_in_facts_with_obj([CA, C1A1], "extra", "relation", None),
                         find_in_facts_with_obj([BC, B1C1], "extra", "relation", None)}

                update_facts([triangle1, triangle2], k, roots, "relation")
                update_facts([triangle2, triangle1], 1 / k, roots, "relation")

                consequences_of_similarity(AB, A1B1, BC, B1C1, CA, C1A1, BCA, B1C1A1, CAB, C1A1B1, ABC, A1B1C1, k)


# Проверяет все треугольники и ищет среди них подобные и равные перебирая вершины одного из треугольников всеми возможными способами
def fix_all_triangles():
    isosceles_triangles()
    for triangle1 in tp.solver_data.polygons:
        if len(triangle1.points) == 3:
            for triangle2 in tp.solver_data.polygons:
                if len(triangle2.points) == 3 and triangle1 != triangle2:
                    [C, A, B, AB, BC, CA, BCA, CAB, ABC] = search_triangle(triangle1)
                    [C1, A1, B1, A1B1, B1C1, C1A1, B1C1A1, C1A1B1, A1B1C1] = search_triangle(triangle2)

                    similaritys_triangles(triangle1, triangle2, AB, CA, BC, BCA, ABC, CAB, A1B1, B1C1, C1A1, B1C1A1, C1A1B1, A1B1C1)
                    similaritys_triangles(triangle1, triangle2, AB, BC, CA, BCA, CAB, ABC, A1B1, B1C1, C1A1, B1C1A1, C1A1B1, A1B1C1)
                    similaritys_triangles(triangle1, triangle2, BC, AB, CA, CAB, BCA, ABC, A1B1, B1C1, C1A1, B1C1A1, C1A1B1, A1B1C1)
                    similaritys_triangles(triangle1, triangle2, BC, CA, AB, CAB, ABC, BCA, A1B1, B1C1, C1A1, B1C1A1, C1A1B1, A1B1C1)
                    similaritys_triangles(triangle1, triangle2, CA, AB, BC, ABC, BCA, CAB, A1B1, B1C1, C1A1, B1C1A1, C1A1B1, A1B1C1)
                    similaritys_triangles(triangle1, triangle2, CA, BC, AB, ABC, CAB, BCA, A1B1, B1C1, C1A1, B1C1A1, C1A1B1, A1B1C1)
                    break


# Поиск решения вопроса среди фактов
def find_ans(q):
    for fact in tp.solver_data.facts:
        if len(fact.objects) == len(q.objects):
            for i in range (len(fact.objects)):
                if fact.objects[i].__str__() == q.objects[i].__str__():
                    if fact.fact_type == q.fact_type:
                        return fact.id
    return None


#Добавялет факты типа size
def add_size_fact():
    for fact in tp.solver_data.facts:
        if tp.solver_data.facts[-1].objects[0] in fact.objects and len(fact.objects) != 1:
            indexes = set()
            indexes.add(fact.id)
            indexes.add(tp.solver_data.facts[-1].id)
            value = 0
            obj1, obj2 = fact.objects[0], fact.objects[1]

            if fact.fact_type == "relation":
                if fact.objects[1].size and not fact.objects[0].size:
                    fact.objects[0].size = fact.objects[1].size  * fact.value
                    if isinstance(fact.objects[0], tp.Angle):
                        fact.objects[0].size = fact.objects[0].size % 360
                    update_facts([fact.objects[0]], fact.objects[0].size, indexes, "size")

                elif fact.objects[0].size and not fact.objects[1].size:
                    fact.objects[1].size = fact.objects[0].size * fact.value
                    if isinstance(fact.objects[1], tp.Angle):
                        fact.objects[1].size = fact.objects[1].size % 360
                    update_facts([fact.objects[1]], fact.objects[1].size, indexes, "size")

            if fact.fact_type == "addition" or fact.fact_type == "difference":
                if not fact.value:
                    if tp.solver_data.facts[-1].objects[0] != fact.objects[0]:
                        fact.value.append(tp.solver_data.facts[-1].objects[0].size)
                        indexes.add(tp.solver_data.facts[-1].id)

                        if len(fact.value) == len(fact.objects) + 1:
                            value = sum(fact.value)
                            if isinstance(fact.objects[0], tp.Angle):
                                value = value % 360
                            fact.objects[0].size = value
                            update_facts([fact.objects[0]], value, indexes, "size")

                else:
                    fact.value = [fact.value]
                    fact.value.append(tp.solver_data.facts[-1].objects[0].size)
                    indexes.add(tp.solver_data.facts[-1].id)

                    if len(fact.value) == len(fact.objects) + 1:
                        value = 2 * fact.value[0] - sum(fact.value)
                        if isinstance(fact.objects[0], tp.Angle):
                            value = value % 360
                        for object in fact.objects:
                            if not object.size:
                                object.size = value
                                update_facts([object], value, indexes, "size")


# Возвращает корни данного факта
def return_roots(ind):
    roots = []
    current_index = tp.solver_data.facts[ind].root_facts
    upd_roots = [0]
    while len(upd_roots) != 0:
        new_indexes = set()
        upd_roots = []
        for index in current_index:
            new_indexes |= tp.solver_data.facts[index].root_facts
            upd_roots.append(index)
            roots.append(index)
        current_index = new_indexes
        if len(upd_roots) == 0:
            roots.sort()
            n_roots = []
            for root in roots:
                n_roots.append(tp.solver_data.facts[root])
            return n_roots


# Делает имя объекта красивым
def beautiful_object(object):
    if isinstance(object, tp.Segment) or isinstance(object, tp.Polygon):
        name = ""
        for point in object.points:
            name += point.name
        return name

    elif isinstance(object, tp.Angle):
        for p1 in tp.solver_data.points:
            for p2 in tp.solver_data.points:
                if p2 != p1:
                    for p3 in tp.solver_data.points:
                        if p3 != p1 and p3 != p2:
                            if tp.find_angle_with_points(p1.name, p2.name, p3.name, tp.solver_data) == object:
                                return (p1.name + p2.name + p3.name)
        return f"Angle between rays [{object.rays[0].main_point.name}{list(object.rays[0].points)[0].name}) and [{object.rays[1].main_point.name}{list(object.rays[1].points)[0].name})"


# Делает факт красивым
def beautiful_fact(fact):
    obj = fact.objects
    if fact.fact_type == "relation":
        if isinstance(obj[0], tp.Polygon):
            return (f"{beautiful_object(obj[0])} / {beautiful_object(obj[1])} = {fact.value}")
        else:
            return (f"{beautiful_object(obj[0])} similars {beautiful_object(obj[1])} with ratio {fact.value}")
    elif fact.fact_type == "size":
        if len(fact.root_facts) == 0:
            return (f"{beautiful_object(obj[0])} equals {fact.value} because of task")
        else:
            return (f"{beautiful_object(obj[0])} equals {fact.value}")
    elif fact.fact_type == "addition":
        if not fact.value:
            sums = []
            for i in range(len(fact.objects)):
                if i != 0:
                    sums.append(beautiful_object(obj[i]))
            out = ", ".join(sums)
            if isinstance(fact.objects[0], tp.Angle):
                return f"{beautiful_object(obj[0])} equals sum of:{out} as sum of angles"
            elif isinstance(fact.objects[0], tp.Segment):
                return f"{beautiful_object(obj[0])} equals sum of:{out} as sum of segments"
        else:
            sums = []
            for i in range(len(fact.objects)):
                sums.append(beautiful_object(obj[i]))
            out = ", ".join(sums)
            if isinstance(fact.objects[0], tp.Angle):
                return f"Sum of angles {out} equals {fact.value}"
            elif isinstance(fact.objects[0], tp.Segment):
                return f"Sum of segments {out} equals {fact.value}"


# Печать факта для юзера
def to_str(fact, roots=True):
    out = ""
    if not roots:
        return beautiful_fact(fact)

    else:
        out += beautiful_fact(fact)
        nlist = []
        for root in fact.root_facts:
            nlist.append(f"{beautiful_fact(tp.solver_data.facts[root])}")
        if len(nlist) != 0:
            out += " because of: "
            out += ", ".join(nlist)

    return out


# Сам процесс решения, проверяет все ли вопросы учтены, выводит нужные факты, формирует словарик с нужными фактами
def solving_process():
    global angles2, segments2

    angles2 = [-1] * len(tp.solver_data.angles)
    segments2 = [-1] * len(tp.solver_data.segments)

    pre_work()

    first()

    fix_all_angles()

    q_indexes = set()

    while len(q_indexes) != len(tp.solver_data.questions):
        for q in tp.solver_data.questions:

            if find_ans(q):
                q_indexes.add(find_ans(q))
            print(0)
            fix_all_triangles()
            add_size_fact()


    return_facts = dict()

    for q_ind in q_indexes:
        return_facts[tp.solver_data.facts[q_ind]] = return_roots(q_ind)


    return return_facts
