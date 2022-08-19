import triangle_drawer as tr
from math import *


def check_if_positive(sides, angles):
    for side in sides:
        if side and side <= 0:
            return False

    for angle in angles:
        if angle and angle <= 0:
            return False

    return True


def check_angles_of_triangle(angles):
    try:
        if abs(sum(angles) - 180) > 0.001:
            return False

    except Exception:
        if sum(list(filter(lambda x: x, angles))) >= 180:
            return False

    return True


def check_triangle_inequality(sides):
    try:
        if max(sides) * 2 < sum(sides):
            return True

        return False

    except Exception:
        return True


def check_correspondence(sides, angles):
    answer = True

    if ((sides[0] != None) and (sides[1] != None) and (angles[0] != None) and (angles[1] != None)):
        if (((sides[0] > sides[1]) and (angles[0] <= angles[1])) or ((sides[0] == sides[1]) and (angles[0] != angles[1])) or ((sides[0] < sides[1]) and (angles[0] >= angles[1]))):
            answer = False
        if (sides[2] != None):
            a = 180 - angles[0] - angles[1]
            if (((sides[2] > sides[0]) and (a <= angles[0])) or ((sides[2] < sides[0]) and (a >= angles[0])) or ((sides[2] == sides[0]) and (a != angles[0])) or ((sides[2] > sides[1]) and (a <= angles[1])) or ((sides[2] < sides[1]) and (a >= angles[1])) or ((sides[2] == sides[1]) and (a != angles[1]))):
                answer = False
    if ((sides[0] != None) and (sides[2] != None) and (angles[0] != None) and (angles[2] != None)):
        if (((sides[0] > sides[2]) and (angles[0] <= angles[2])) or ((sides[0] == sides[2]) and (angles[0] != angles[2])) or ((sides[0] < sides[2]) and (angles[0] >= angles[2]))):
            answer = False
        if (sides[1] != None):
            a = 180 - angles[0] - angles[2]
            if (((sides[1] > sides[0]) and (a <= angles[0])) or ((sides[1] < sides[0]) and (a >= angles[0])) or ((sides[1] == sides[0]) and (a != angles[0])) or ((sides[1] > sides[2]) and (a <= angles[2])) or ((sides[1] < sides[2]) and (a >= angles[2])) or ((sides[1] == sides[2]) and (a != angles[2]))):
                answer = False
    if ((sides[1] != None) and (sides[2] != None) and (angles[1] != None) and (angles[2] != None)):
        if (((sides[1] > sides[2]) and (angles[1] <= angles[2])) or ((sides[1] == sides[2]) and (angles[1] != angles[2])) or ((sides[1] < sides[2])and(angles[1] >= angles[2]))):
            answer = False
        if (sides[0] != None):
            a = 180 - angles[1] - angles[2]
            if (((sides[0] > sides[1]) and (a <= angles[1])) or ((sides[0] < sides[1]) and (a >= angles[1])) or ((sides[0] == sides[1]) and (a != angles[1])) or ((sides[0] > sides[2]) and (a <= angles[2])) or ((sides[0] < sides[2]) and (a >= angles[2])) or ((sides[0] == sides[2]) and (a != angles[2]))):
                answer = False
    return answer


def check_law_of_cos(sides, angles):
    if sides[0] and sides[1] and sides[2]:
        x = 0.5 * ((sides[0] * sides[0]) + (sides[1] * sides[1]) + (sides[2] * sides[2]))
        if angles[0]:
            n = round((x - (sides[0] * sides[0])) / (sides[1] * sides[2]), 3)
            if round((cos(radians(angles[0].value))), 3) != n:
                return False
        if angles[1]:
            n = round((x - (sides[1] * sides[1])) / (sides[0] * sides[2]), 3)
            if round((cos(radians(angles[1].value))), 3) != n:
                return False
        if angles[2]:
            n = round((x - (sides[2] * sides[2])) / (sides[1] * sides[0]), 3)
            if round((cos(radians(angles[2].value))), 3) != n:
                return False

    return True


def check_angle_not_between_sides(sides, angles):
    for i in range(3):
        if angles[i]:
            if sides[i] and sides[i - 1]:
                return try_create_triangle_with_two_sides_and_angle_not_between_them(sides[i - 1], sides[i], angles[i])
            if sides[i] and sides[(i + 1) % 3]:
                return try_create_triangle_with_two_sides_and_angle_not_between_them(sides[(i + 1) % 3], sides[i], angles[i])

    else:
        return True


def try_create_triangle_with_two_sides_and_angle_not_between_them(a, c, gamma):
    C = tr.MyPoint(0, 0)
    B = tr.MyPoint(a, 0)

    l = tr.LineWithTiltAngle(C, gamma)

    try:
        tr.LineAndCircleIntersectionPoints(l, B, c)
        return True

    except Exception:
        return False


def check_triangle(sides, angles):
    if check_if_positive(sides, angles):
        if check_angle_not_between_sides(sides, angles):
            if check_angles_of_triangle(angles):
                if check_triangle_inequality(sides):
                    if check_correspondence(sides, angles):
                        if check_law_of_cos(sides, angles):
                            return True
                        else:
                            return True
                            # return 'Error: Incorrect triangle (The angles do not correspond to the sides of the triangle).'
                    else:
                        return 'Error: Incorrect triangle (The greater side must be opposite to the greater angle).'
                else:
                    return 'Error: Incorrect triangle (The triangle inequality is violated).'
            else:
                return 'Error: Incorrect triangle (The sum of angles of a triangle must equal 180 degrees).'
        else:
            return 'Error: Incorrect triangle (There is no triangle with such sides and angle not between them).'
    else:
        return 'Error: Invalid values (The values of the angles and sides must be positive).'
