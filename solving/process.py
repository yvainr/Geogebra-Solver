import task_parser
from math import*

Similaritys_allowed = True
Proportion_theorem = True
Cos_theorem_allowed = True
Sin_theorem_allowed = True

objects_cnt = 0

ans = task_parser.ans

out = [0]


def create():
    global ans
    cur = ans
    for p1 in task_parser.points:
        for p2 in task_parser.points:
            if p1 != p2:
                s = task_parser.find_segment_with_points(p1.name, p2.name)
                ans = task_parser.ans
                if ans - 1 == cur:
                    s.size = "Neo_update"
                    cur += 1
    for p1 in task_parser.points:
        for p2 in task_parser.points:
            if p1 != p2:
                s = task_parser.find_line_with_points(p1.name, p2.name)
                ans = task_parser.ans
                if ans - 1 == cur:
                    s.size = "Neo_update"
                    cur += 1
                    s.points.add(task_parser.Point("Neo_update"))
    for l1 in task_parser.lines:
        for l2 in task_parser.lines:
            if l1 != l2:
                s = task_parser.find_angle_with_lines(l1, l2)
                ans = task_parser.ans
                if ans - 1 == cur:
                    s.size = "Neo_update"
                    cur += 1
                    s.size = "Neo_update"
    x = task_parser.json_create()

    return x

x = create()

def find_angle_with_lines(l1, l2):
    global objects_cnt
    for angle in x:
        if x[angle]["type"] == "angle":
            if x[angle]['angle_between_lines'] == [l1, l2]:
                return angle

    for angle in x:
        if x[angle]["type"] == "neo_angle":
            if x[angle]['angle_between_lines'] == [l1, l2]:
                x[angle]["type"] = "angle"
                return angle

def find_segment_with_points(A, B):
    for segment in x:
        if x[segment]["type"] == "segment":
            if x[segment]['points_on_object'] == [A, B] or x[segment]['points_on_object'] == [B, A]:
                return segment
    for segment in x:
        if x[segment]["type"] == "neo_segment":
            if x[segment]['points_on_object'] == [A, B] or x[segment]['points_on_object'] == [B, A]:
                x[segment]["type"] = "segment"
                return segment

def find_line_with_points(A, B):
    for segment in x:
        if x[segment]["type"] == "line":
            if x[segment]['points_on_object'] == [A, B] or x[segment]['points_on_object'] == [B, A]:
                return segment

    for segment in x:
        if x[segment]["type"] == "neo_line":
            if x[segment]['points_on_object'] == [A, B] or x[segment]['points_on_object'] == [B, A]:
                x[segment]["type"] = "line"
                return segment

def similaritys():
    for segment1 in x:
        if x[segment1]['type'] == "segment" or x[segment1]['type'] == "angle":
            for segment2 in x:
                if x[segment2]['type'] == x[segment1]['type'] and segment1 != segment2:
                    if segment1 in x[segment2]['relations']:
                        if x[segment1]["size"]:
                            x[segment2]["size"] = x[segment1]["size"] / x[segment2]['relations'][segment1]
                        if x[segment2]["size"]:
                            x[segment1]["size"] = x[segment2]["size"] / x[segment1]['relations'][segment2]

def fix_vertical_angles():
    for l1 in x:
        if x[l1]['type'] == "line":
            for l2 in x:
                if x[l2]['type'] == "line" and l2 != l1:
                    if x[find_angle_with_lines(l2, l1)]["size"] and not x[find_angle_with_lines(l1, l2)]["size"]:
                        angle_between_two_lines = x[find_angle_with_lines(l2, l1)]["size"]
                        for second_angle in x:
                            if x[second_angle]['type'] == "angle" and [l1, l2] == x[second_angle]['angle_between_lines']:
                                x[second_angle]["size"] = 180 - angle_between_two_lines
                    if x[find_angle_with_lines(l1, l2)]["size"] and not x[find_angle_with_lines(l2, l1)]["size"]:
                        angle_between_two_lines = x[find_angle_with_lines(l1, l2)]["size"]
                        for second_angle in x:
                            if x[second_angle]['type'] == "angle" and [l2, l1] == x[second_angle]['angle_between_lines']:
                                x[second_angle]["size"] = 180 - angle_between_two_lines

def correct_three_angles(l1, l2, l3):
    if x[find_angle_with_lines(l1, l2)]["size"] and x[find_angle_with_lines(l2, l3)]["size"] and x[find_angle_with_lines(l1, l3)]["size"]:
        for third_angle in x:
            if third_angle['type'] == "angle" and [l1, l3] == x[third_angle]['angle_between_lines']:
                x[third_angle]["size"] = (x[find_angle_with_lines(l2, l3)]["size"] + x[find_angle_with_lines(l1, l2)]["size"]) % 180


def fix_all_angles():
    similaritys()
    fix_vertical_angles()
    for l1 in x:
        if x[l1]['type'] == "line":
            for l2 in x:
                if x[l2]['type'] == "line" and l2 != l1:
                    for l3 in x:
                        if x[l3]['type'] == "line" and l3 != l2 and l3 != l1:
                            if not x[find_angle_with_lines(l1, l3)]["size"]:
                                correct_three_angles(l1, l2, l3)
                            if not x[find_angle_with_lines(l2, l3)]["size"]:
                                correct_three_angles(l2, l1, l3)
                            if not x[find_angle_with_lines(l2, l1)]["size"]:
                                correct_three_angles(l2, l3, l1)
    fix_vertical_angles()
def search_triangle(triangle):
    A, B, C = x[triangle]['points_on_object'][0], x[triangle]['points_on_object'][1], x[triangle]['points_on_object'][2]
    AB = find_segment_with_points(A, B)
    BC = find_segment_with_points(B, C)
    CA = find_segment_with_points(C, A)

    A2B2 = find_line_with_points(A, B)
    B2C2 = find_line_with_points(B, C)
    C2A2 = find_line_with_points(C, A)

    ABC = find_angle_with_lines(A2B2, B2C2)
    BCA = find_angle_with_lines(B2C2, C2A2)
    CAB = find_angle_with_lines(C2A2, A2B2)


    return [A, B, C, AB, BC, CA, ABC, BCA, CAB]

def correct_size(ABC, BCA, AB, CA):
    if x[ABC]["size"] == x[BCA]["size"] and x[ABC]["size"]:
        if x[CA]["size"]:
            x[AB]["size"] = x[CA]["size"]
        elif x[AB]["size"]:
            x[CA]["size"] = x[AB]["size"]

def equals(AB, BC):
    if x[AB]["size"] == x[BC]["size"] or not x[AB]["size"] or not x[BC]["size"]:
        return True

def equal_them(AB, BC):
    if AB:
        x[BC]["size"] = x[AB]["size"]
    if BC:
        x[AB]["size"] = x[BC]["size"]

def isosceles_triangles():
    for triangle in x:
        if x[triangle]['type'] == "polygon" and len(x[triangle]['points_on_object']) == 3:
            [A, B, C, AB, BC, CA, ABC, BCA, CAB] = search_triangle(triangle)
            correct_size(ABC, BCA, AB, CA)
            correct_size(ABC, CAB, BC, CA)
            correct_size(CAB, BCA, BC, AB)

def equality_triangles(triangle1, triangle2, A, B, C, A1, B1, C1, AB, BC, CA, BCA, CAB, ABC, A1B1, B1C1, C1A1, B1C1A1, C1A1B1, A1B1C1):
    if (x[AB]["size"] == x[A1B1]["size"] and x[AB]["size"] and x[BC]["size"] and x[BC]["size"] == x[B1C1]["size"] and x[ABC]["size"] and x[ABC]["size"] == x[A1B1C1]["size"]) \
            or (x[AB]["size"] and x[CA]["size"] and x[CAB]["size"] and x[AB]["size"] == x[A1B1]["size"] and x[CA]["size"] == x[C1A1]["size"] and x[CAB]["size"] == x[C1A1B1]["size"]) \
            or (x[CA]["size"] and x[BC]["size"] and x[BCA]["size"] and x[CA]["size"] == x[C1A1]["size"] and x[BC]["size"] == x[B1C1]["size"] and x[BCA]["size"] == x[B1C1A1]["size"]):
        equal_them(AB, A1B1)
        equal_them(BC, B1C1)
        equal_them(CA, C1A1)
        equal_them(BCA, B1C1A1)
        equal_them(CAB, C1A1B1)
        equal_them(ABC, A1B1C1)
        if out[0] == 0:
            out[0] = f"Треугольник {x[A]['name']}{x[B]['name']}{x[C]['name']} равен треугольнику {x[A1]['name']}{x[B1]['name']}{x[C1]['name']} по первому признаку равенства треугольников"
    if (x[AB]["size"] and x[CAB]["size"] and x[ABC]["size"] and x[AB]["size"] == x[A1B1]["size"] and x[CAB]["size"] == x[C1A1B1]["size"] and x[ABC]["size"] == x[A1B1C1]["size"])\
            or (x[BC]["size"] and x[ABC]["size"] and x[BCA]["size"] and x[BC]["size"] == x[B1C1]["size"] and x[ABC]["size"] == x[A1B1C1]["size"] and x[BCA]["size"] == x[B1C1A1]["size"])\
            or (x[CA]["size"] and x[CAB]["size"] and x[BCA]["size"] and x[CA]["size"] == x[C1A1]["size"] and x[CAB]["size"] == x[C1A1B1]["size"] and x[BCA]["size"] == x[B1C1A1]["size"]):
        equal_them(AB, A1B1)
        equal_them(BC, B1C1)
        equal_them(CA, C1A1)
        equal_them(BCA, B1C1A1)
        equal_them(CAB, C1A1B1)
        equal_them(ABC, A1B1C1)
        if out[0] == 0:
            out[0] = f"Треугольник {x[A]['name']}{x[B]['name']}{x[C]['name']} равен треугольнику {x[A1]['name']}{x[B1]['name']}{x[C1]['name']} по второму признаку равенства треугольников"
    if (x[AB]["size"] and x[BC]["size"] and x[CA]["size"] and x[AB]["size"] == x[A1B1]["size"] and x[BC]["size"] == x[B1C1]["size"] and x[CA]["size"] == x[C1A1]["size"]):
        equal_them(AB, A1B1)
        equal_them(BC, B1C1)
        equal_them(CA, C1A1)
        equal_them(BCA, B1C1A1)
        equal_them(CAB, C1A1B1)
        equal_them(ABC, A1B1C1)
        if out[0] == 0:
            out[0] = f"Треугольник {x[A]['name']}{x[B]['name']}{x[C]['name']} равен треугольнику {x[A1]['name']}{x[B1]['name']}{x[C1]['name']} по третьему признаку равенства треугольников"

def full_equal_triangles():
    for triangle1 in x:
        if x[triangle1]['type'] == "polygon" and len(x[triangle1]['points_on_object']) == 3:
            for triangle2 in x:
                if x[triangle2]['type'] == "polygon" and len(x[triangle2]['points_on_object']) == 3 and x[triangle1] != x[triangle2]:
                    [A, B, C, AB, BC, CA, ABC, BCA, CAB] = search_triangle(triangle1)
                    [A1, B1, C1, A1B1, B1C1, C1A1, A1B1C1, B1C1A1, C1A1B1] = search_triangle(triangle2)
                    equality_triangles(triangle1, triangle2, C, B, A, C1, B1, A1, AB, CA, BC, BCA, ABC, CAB, A1B1, C1A1, B1C1, B1C1A1, A1B1C1, C1A1B1)
                    equality_triangles(triangle1, triangle2, C, A, B, C1, B1, A1, AB, BC, CA, BCA, CAB, ABC, A1B1, C1A1, B1C1, B1C1A1, A1B1C1, C1A1B1)
                    equality_triangles(triangle1, triangle2, A, C, B, C1, B1, A1, BC, AB, CA, CAB, BCA, ABC, A1B1, C1A1, B1C1, B1C1A1, A1B1C1, C1A1B1)
                    equality_triangles(triangle1, triangle2, A, B, C, C1, B1, A1, BC, CA, AB, CAB, ABC, BCA, A1B1, C1A1, B1C1, B1C1A1, A1B1C1, C1A1B1)
                    equality_triangles(triangle1, triangle2, B, C, A, C1, B1, A1, CA, AB, BC, ABC, BCA, CAB, A1B1, C1A1, B1C1, B1C1A1, A1B1C1, C1A1B1)
                    equality_triangles(triangle1, triangle2, B, A, C, C1, B1, A1, CA, BC, AB, ABC, CAB, BCA, A1B1, C1A1, B1C1, B1C1A1, A1B1C1, C1A1B1)

def solving_process():
    for key in x:
        print(key, x[key])

    iterations = 7
    for i in range(iterations):
        fix_all_angles()
        isosceles_triangles()
        full_equal_triangles()
    if out[0] != 0:
        print(*out)

    for key in x:
        print(key, x[key])

solving_process()
