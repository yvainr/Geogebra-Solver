from task_parser import*

Proportion_theorem = True
Cos_theorem_allowed = True
Sin_theorem_allowed = True

#Индекс последнего добавленного факта

ind = 0
facts = []
facts_indexes = []

not_none_angles = []
#Это нужно чтобы не перебирать None углы, если угол в результате вычислений становится не None - он сюда добавляется

similarity = []

#Неприятная функция, добавляющая все возможные прямые, отрезки, треугольники и углы
def first():
    global ind
    #Перебирает тройки и двойки точек, проверяет существует ли прямая (отрезок) с данными двумя точками, существует ли треугольник с этими тремя точками
    for p1 in points:
        for p2 in points:
            if p1 != p2:
                further_line = True
                further_segment = True
                for p3 in points:
                    if p3 != p1 and p3 != p2:
                        further = True
                        for polyg in polygons:
                            if len(polyg.points) == 3:
                                if p1 in polyg.points and p2 in polyg.points and p3 in polyg.points:
                                    further = False
                                    break
                        if further:
                            polygons.append(Polygon([p1, p2, p3]))
                for line in lines:
                    if {p1, p2} == line.points:
                        further_line = False
                        break
                if further_line:
                    lines.append(Line({p1, p2}))
                for segment in segments:
                    if {p1, p2} == segment.points:
                        further_segment = False
                        break
                if further_segment:
                    segments.append(Segment(p1, p2))
    #Перебирает пары прямых, проверяет существеут ли между ними угол, если нет - добавляет.
    for l1 in lines:
        for l2 in lines:
            futher_angle = True
            if l1 != l2:
                for ang in angles:
                    if [l1, l2] == ang.lines:
                        futher_angle = False
                if futher_angle:
                    angles.append(Angle(l1, l2))
                    angles.append(Angle(l2, l1))
    #Добавляет факты с отрезками и углами
    for ang in angles:
        if ang.size:
            not_none_angles.append(ang)
            facts.append(Fact(ind, -1, "size", [ang], ang.size))
            ind += 1

    for seg in segments:
        if seg.size:
            facts.append(Fact(ind, -1, "size", [seg], seg.size))
            ind += 1

first()

#Находит факт по объектам в нём (если strict - то конкретно с этими объектами, иначе он находит факт где мы находим значение этого объекта)
def find_in_facts_with_obj(obj, not_strict = False):
    if not not_strict:
        for x in facts:
            if {x.objects} == {obj}:
                return x.index
    else:
        for x in facts:
            if x.objects[0] == obj[0]:
                return x.index

#Обновляет факты
def update_facts(ind, fact_obj, value, roofs, reason):
    facts.append(Fact(ind, -1, reason, fact_obj, value))
    for roof in roofs:
        facts[roof].following_facts.append(ind)
        facts[-1].root_facts.add(roof)
    ind += 1

#Обсчитывает вертикальные углы
def fix_vertical_angles():
    #Проверяет угол (не None) и если смежный с ним не определен - считает его
    for ang_1 in not_none_angles:
        for ang_2 in angles:
            if ang_1 != ang_2:
                lines1 = ang_1.lines
                lines2 = ang_2.lines
                if set(lines1) == set(lines2):
                    if not ang_2.size:
                        ang_2.size = 180 - ang_1.size
                        not_none_angles.append(ang_2)

                        roof1 = find_in_facts_with_obj([ang_1], "not")
                        roofs = {roof1}

                        update_facts(ind, [ang_1, ang_2], ang_2.size, roofs, "Мы еще не добавили Смежные углы")

#Рассматривает как и вертикальные углы, так и суммы двух соседних углов, в результате чего корректирует все углы
def fix_all_angles():
    #Рассматривает три угла, где 2 известны и лежат в not_none_angles, а третий - неизвестен и равен их сумме
    fix_vertical_angles()
    for ang1 in not_none_angles:
        for ang2 in not_none_angles:
            if ang1 != ang2 :
                for ang3 in angles:
                    if ang3 != ang2 and ang3 != ang1 and not ang3:
                        lines1 = ang1.lines
                        lines2 = ang2.lines
                        lines3 = ang3.lines
                        if lines1[1] == lines2[0] and [lines[0], lines2[1]] == lines3:
                            ang3.size = (ang1 + ang2) % 180
                            not_none_angles.append(ang3)

                            roof1, roof2 = find_in_facts_with_obj([ang1], "not"), find_in_facts_with_obj([ang2], "not")
                            roofs = {roof1, roof2}

                            update_facts(ind, [ang3, ang1, ang2], ang3.size, roofs, "Мы еще не добавили Сумма двух углов")

    fix_vertical_angles()

#Выдает все данные об этом треугольнике
def search_triangle(triangle):
    A, B, C = triangle.points[0], triangle.points[1], triangle.points[2]

    AB = find_segment_with_points(A.name, B.name)

    BC = find_segment_with_points(B.name, C.name)
    CA = find_segment_with_points(C.name, A.name)

    A2B2 = find_line_with_points(A.name, B.name)
    B2C2 = find_line_with_points(B.name, C.name)
    C2A2 = find_line_with_points(C.name, A.name)

    ABC = find_angle_with_lines(A2B2, B2C2)
    BCA = find_angle_with_lines(B2C2, C2A2)
    CAB = find_angle_with_lines(C2A2, A2B2)

    return [A, B, C, AB, BC, CA, ABC, BCA, CAB]

#Корректирует равенства сторон и углов в равнобедренном треугольнике
def correct_size(ABC, BCA, AB, CA):
    if ABC.size == BCA.size and ABC.size:
        if CA.size and not AB.size:
            AB.size = CA.size

            roof1, roof2 = find_in_facts_with_obj([ABC, BCA]), find_in_facts_with_obj([CA], "not")
            roofs = {roof1, roof2}

            update_facts(ind, [AB, CA], AB.size, roofs, "relation")

        elif AB.size and not CA.size:
            CA.size = AB.size

            roof1, roof2 = find_in_facts_with_obj([ABC, BCA]), find_in_facts_with_obj([AB], "not")
            roofs = {roof1, roof2}

            update_facts(ind, [CA, AB], CA.size, roofs, "relation")

    if AB.size == CA.size and AB.size:
        if BCA.size and not ABC.size:
            ABC.size = BCA.size
            not_none_angles.append(ABC)

            roof1, roof2 = find_in_facts_with_obj([AB, CA]), find_in_facts_with_obj([BCA], "not")
            roofs = {roof1, roof2}

            update_facts(ind, [ABC, BCA], ABC.size, roofs, "relation")

        elif ABC.size and not BCA.size:
            BCA.size = ABC.size
            not_none_angles.append(BCA)

            roof1, roof2 = find_in_facts_with_obj([AB, CA]), find_in_facts_with_obj([ABC], "not")
            roofs = {roof1, roof2}

            update_facts(ind, [BCA, ABC], BCA.size, roofs, "relation")

#Проверяет равенство величин объектов, при их не None_овости
def equal(AB, BC):
    if AB.size == BC.size and AB.size:
        return True
    else:
        return False

#Делает углы, где один из них None, а другой - нет, равными (из подобия треугольников)
def equal_them(A, B, fact):
    if A.size and not B.size:
        B.size = A.size

        update_facts(ind, [B, A], A.size, fact, "relation")

        not_none_angles.append(B)

    if B.size and not A.size:
        A.size = B.size
        not_none_angles.append(A)

        update_facts(ind, [A, B], B.size, fact, "relation")

        not_none_angles.append(A)

#Делает стороны, где один из них None, а другой - нет, подобными (из подобия треугольников)
def simil_them(AB, A1B1, k, fact):
    if AB.size and not A1B1.size:
        A1B1.size = AB.size / k

        update_facts(ind, [A1B1, AB], A1B1.size, fact, "relation")

    if A1B1.size and not AB.size:
        AB.size = A1B1.size * k

        update_facts(ind, [AB, A1B1], AB.size, fact, "relation")

#Находит все стороны и углы, которые может из равнобедренности, во всех р/б треугольниках
def isosceles_triangles():
    for triangle in polygons:
        if len(triangle.points) == 3:
            [A, B, C, AB, BC, CA, ABC, BCA, CAB] = search_triangle(triangle)
            correct_size(ABC, BCA, AB, CA)
            correct_size(ABC, CAB, BC, CA)
            correct_size(CAB, BCA, BC, AB)
 
#Возвращает отношение двух объектов, если это нужно (когда они оба не None)
def similarity_if_not_None(AB, BC):
    if AB.size and BC.size:
        return AB.size / BC.size
    else:
        return None

#Добавляет новые факты следующие из подобия треугольников
def consequences_of_similarity(AB, A1B1, BC, B1C1, CA, C1A1, BCA, B1C1A1, CAB, C1A1B1, ABC, A1B1C1):
    k = similarity_if_not_None(AB, A1B1)
    if not k:
        k = similarity_if_not_None(BC, B1C1)
        if not k:
            k = similarity_if_not_None(CA, C1A1)
    fact = ind
    simil_them(AB, A1B1, k, fact)
    simil_them(BC, B1C1, k, fact)
    simil_them(CA, C1A1, k, fact)
    equal_them(BCA, B1C1A1, fact)
    equal_them(CAB, C1A1B1, fact)
    equal_them(ABC, A1B1C1, fact)

#Проверяет все возможные варианты подобия трекугольников, если вершины для подобия указаны в правильном порядке
def similaritys_triangles(triangle1, triangle2, A, B, C, A1, B1, C1, AB, BC, CA, BCA, CAB, ABC, A1B1, B1C1, C1A1, B1C1A1, C1A1B1, A1B1C1):
    for data in facts:
        if data.objects == [triangle1, triangle2] or data.objects == [triangle2, triangle1]:
            return 0

    if (similarity_if_not_None(AB, A1B1) == similarity_if_not_None(BC, B1C1) and equal(ABC, A1B1C1) and similarity_if_not_None(AB, A1B1)):
        roof1, roof2, roof3 = find_in_facts_with_obj([AB, A1B1]), find_in_facts_with_obj([ABC, A1B1C1]), find_in_facts_with_obj([BC, B1C1])
        roofs = {roof1, roof2, roof3}

        update_facts(ind, [triangle1, triangle2], None, roofs, "relation")

        consequences_of_similarity(AB, A1B1, BC, B1C1, CA, C1A1, BCA, B1C1A1, CAB, C1A1B1, ABC, A1B1C1)

    elif (similarity_if_not_None(AB, A1B1) == similarity_if_not_None(CA, C1A1) and equal(CAB, C1A1B1) and similarity_if_not_None(AB, A1B1)):
        roof1, roof2, roof3 = find_in_facts_with_obj([AB, A1B1]), find_in_facts_with_obj([CAB, C1A1B1]), find_in_facts_with_obj([CA, C1A1])
        roofs = {roof1, roof2, roof3}

        update_facts(ind, [triangle1, triangle2], None, roofs, "relation")

        consequences_of_similarity(AB, A1B1, BC, B1C1, CA, C1A1, BCA, B1C1A1, CAB, C1A1B1, ABC, A1B1C1)

    elif (similarity_if_not_None(BC, B1C1) ==  similarity_if_not_None(CA, C1A1) and equal(BCA, B1C1A1) and similarity_if_not_None(BC, B1C1)):
        roof1, roof2, roof3 = find_in_facts_with_obj([BC, B1C1]), find_in_facts_with_obj([BCA, B1C1A1]), find_in_facts_with_obj([CA, C1A1])
        roofs = {roof1, roof2, roof3}

        update_facts(ind, [triangle1, triangle2], None, roofs, "relation")

        consequences_of_similarity(AB, A1B1, BC, B1C1, CA, C1A1, BCA, B1C1A1, CAB, C1A1B1, ABC, A1B1C1)

    elif (equal(ABC, A1B1C1) and equal(CAB, C1A1B1) and similarity_if_not_None(AB, A1B1)):
        roof1, roof2, roof3 = find_in_facts_with_obj([ABC, A1B1C1]), find_in_facts_with_obj([CAB, C1A1B1]), find_in_facts_with_obj([AB, A1B1])
        roofs = {roof1, roof2, roof3}

        update_facts(ind, [triangle1, triangle2], None, roofs, "relation")

        consequences_of_similarity(AB, A1B1, BC, B1C1, CA, C1A1, BCA, B1C1A1, CAB, C1A1B1, ABC, A1B1C1)

    elif (equal(ABC, A1B1C1) and equal(BCA, B1C1A1) and similarity_if_not_None(BC, B1C1)):
        roof1, roof2, roof3 = find_in_facts_with_obj([ABC, A1B1C1]), find_in_facts_with_obj([BCA, B1C1A1]), find_in_facts_with_obj([BC, B1C1])
        roofs = {roof1, roof2, roof3}

        update_facts(ind, [triangle1, triangle2], None, roofs, "relation")

        consequences_of_similarity(AB, A1B1, BC, B1C1, CA, C1A1, BCA, B1C1A1, CAB, C1A1B1, ABC, A1B1C1)

    elif (similarity_if_not_None(CA, C1A1) == similarity_if_not_None(AB, A1B1) and similarity_if_not_None(BC, B1C1) == similarity_if_not_None(AB, A1B1) and similarity_if_not_None(AB, A1B1)):
        roof1, roof2, roof3 = find_in_facts_with_obj([AB, A1B1]), find_in_facts_with_obj([CA, C1A1]), find_in_facts_with_obj([BC, B1C1])
        roofs = {roof1, roof2, roof3}

        update_facts(ind, [triangle1, triangle2], None, roofs, "relation")

        consequences_of_similarity(AB, A1B1, BC, B1C1, CA, C1A1, BCA, B1C1A1, CAB, C1A1B1, ABC, A1B1C1)

#Проверяет все треугольники и ищет среди них подобные и равные перебирая вершины одного из треугольников всеми возможными способами
def fix_all_triangles():
    isosceles_triangles()
    for triangle1 in polygons:
        if len(triangle1.points) == 3:
            for triangle2 in polygons:
                if len(triangle2.points) == 3 and triangle1 != triangle2:
                    [A, B, C, AB, BC, CA, ABC, BCA, CAB] = search_triangle(triangle1)
                    [A1, B1, C1, A1B1, B1C1, C1A1, A1B1C1, B1C1A1, C1A1B1] = search_triangle(triangle2)
                    similaritys_triangles(triangle1, triangle2, C, B, A, C1, B1, A1, AB, CA, BC, BCA, ABC, CAB, A1B1, C1A1, B1C1, B1C1A1, A1B1C1, C1A1B1)
                    similaritys_triangles(triangle1, triangle2, C, A, B, C1, B1, A1, AB, BC, CA, BCA, CAB, ABC, A1B1, C1A1, B1C1, B1C1A1, A1B1C1, C1A1B1)
                    similaritys_triangles(triangle1, triangle2, A, C, B, C1, B1, A1, BC, AB, CA, CAB, BCA, ABC, A1B1, C1A1, B1C1, B1C1A1, A1B1C1, C1A1B1)
                    similaritys_triangles(triangle1, triangle2, A, B, C, C1, B1, A1, BC, CA, AB, CAB, ABC, BCA, A1B1, C1A1, B1C1, B1C1A1, A1B1C1, C1A1B1)
                    similaritys_triangles(triangle1, triangle2, B, C, A, C1, B1, A1, CA, AB, BC, ABC, BCA, CAB, A1B1, C1A1, B1C1, B1C1A1, A1B1C1, C1A1B1)
                    similaritys_triangles(triangle1, triangle2, B, A, C, C1, B1, A1, CA, BC, AB, ABC, CAB, BCA, A1B1, C1A1, B1C1, B1C1A1, A1B1C1, C1A1B1)
                    break

#Сам процесс решения
def solving_process():
    iterations = 1
    for i in range(iterations):
        fix_all_angles()
        fix_all_triangles()

solving_process()