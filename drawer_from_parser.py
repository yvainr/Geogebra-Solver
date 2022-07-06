import task_parser
import geogebra_html_generator
from math import*

points_of_triangle = []
names = []

x = taskp.json_create()

for object in x:
    t = x[object]
    if t['type'] == "polygon":
        for point in t['points_on_object']:
            names.append(x[point]['name'])
            points_of_triangle.append(point)

angle_default = 70

first_angle = taskp.find_angle_with_points(points_of_triangle[1],points_of_triangle[0], points_of_triangle[2]).size
second_angle = taskp.find_angle_with_points(points_of_triangle[0],points_of_triangle[1], points_of_triangle[2]).size
third_angle = taskp.find_angle_with_points(points_of_triangle[1],points_of_triangle[2], points_of_triangle[0]).size

first_segment = taskp.find_segment_with_points(points_of_triangle[1],points_of_triangle[2]).size
second_segment = taskp.find_segment_with_points(points_of_triangle[0],points_of_triangle[2]).size
third_segment = taskp.find_segment_with_points(points_of_triangle[1],points_of_triangle[0]).size

first_angle = 80
second_angle = 20
first_segment = 3

def perevod(ugol):
    if ugol != None:
        ugol *= 2 * pi / 180

first_angle = perevod(first_angle)
second_angle = perevod(second_angle)
third_angle = perevod(third_angle)

def izvesten_otrezok(name,first_segment, names_1, names_2, second_angle, third_angle, second_segment, third_segment):
    global output_html
    if first_segment == None:
        first_segment = 1
    first_str = names_1 + "(" + str(first_segment / 2) + ", 0)"
    second_str = names_2 + "(" + str(first_segment * (-1) / 2) + ", 0)"
    x = [0, first_segment / 2, first_segment * (-1) / 2]
    if third_segment != None and second_angle != None:
        third_str = "w1 = Circle(" + str(names_1) + "," + str(third_segment) + ")"

        y_d = x[1] * tan(second_angle)
        fourth_str = "l = Line(" + str(names_1) + ",(" + str(0) + "," + str(y_d) + "))"

        fith_str = str(name) + "_{1} = Intersect(l, w1)"
    elif second_segment != None and third_angle != None:
        third_str = "w1 = Circle(" + str(names_2) + "," + str(second_segment) + ")"

        y_d = x[2] * tan(third_angle) * -1
        fourth_str = "l = Line(" + str(names_2) + ",(" + str(0) + "," + str(y_d) + "))"

        fith_str = str(name) + "_{1} = Intersect(l, w1)"
    elif third_angle != None and second_angle != None:
        y_d = x[1] * tan(second_angle)
        third_str = "l = Line(" + str(names_1) + ",(" + str(0) + "," + str(y_d) + "))"

        y_d = x[2] * tan(third_angle) * -1
        fourth_str = "l1 = Line(" + str(names_2) + ",(" + str(0) + "," + str(y_d) + "))"

        fith_str = str(name) + "_{1} = intersect(l1, l)"
    elif third_segment != None and second_segment != None:
        third_str = "w1 = Circle(" + str(names_1) + "," + str(third_segment) + ")"

        fourth_str = "w2 = Circle(" + str(names_2) + "," + str(second_segment) + ")"

        fith_str = str(name) + "_{1} = Intersect(w1, w2)"
    elif second_segment != None and second_angle != None:
        third_str = "w1 = Circle(" + str(names_2) + "," + str(second_segment) + ")"

        y_d = x[1] * tan(second_angle)
        fourth_str = "l = Line(" + str(names_1) + ",(" + str(0) + "," + str(y_d) + "))"

        fith_str = str(name) + "_{1} = Intersect(l, w1)"
    elif third_segment != None and third_angle != None:
        third_str = "w1 = Circle(" + str(names_1) + "," + str(third_segment) + ")"

        y_d = x[2] * tan(second_angle) * -1
        fourth_str = "l = Line(" + str(names_2) + ",(" + str(0) + "," + str(y_d) + "))"

        fith_str = str(name) + "_{1} = Intersect(l, w1)"
    elif third_segment != None:
        third_str = "w1 = Circle(" + str(names_1) + "," + str(third_segment) + ")"

        second_angle = 1
        y_d = x[1] * tan(second_angle)
        fourth_str = "l = Line(" + str(names_1) + ",(" + str(0) + "," + str(y_d) + "))"

        fith_str = str(name) + "_{1} = Intersect(l, w1)"
    elif second_segment != None:
        third_str = "w1 = Circle(" + str(names_2) + "," + str(second_segment) + ")"

        third_angle = 1

        y_d = x[2] * tan(third_angle) * -1
        fourth_str = "l = Line(" + str(names_2) + ",(" + str(0) + "," + str(y_d) + "))"

        fith_str = str(name) + "_{1} = Intersect(l, w1)"
    elif third_angle != None:
        second_angle = 1
        y_d = x[1] * tan(second_angle)
        third_str = "l = Line(" + str(names_1) + ",(" + str(0) + "," + str(y_d) + "))"

        y_d = x[2] * tan(third_angle) * -1
        fourth_str = "l1 = Line(" + str(names_2) + ",(" + str(0) + "," + str(y_d) + "))"

        fith_str = str(name) + "_{1} = Intersect(l1, l)"
    elif second_angle != None:
        third_angle = 1
        y_d = x[1] * tan(second_angle)
        third_str = "l = Line(" + str(name) + ",(" + str(0) + "," + str(y_d) + "))"

        y_d = x[2] * tan(third_angle) * -1
        fourth_str = "l1 = Line(" + str(name) + ",(" + str(0) + "," + str(y_d) + "))"

        fith_str = str(name) + "_{1} = Intersect(l1, l)"
    else:
        third_angle = 1
        second_angle = 1

        y_d = x[1] * tan(second_angle)
        third_str = "l = Line(" + str(names_1) + ",(" + str(0) + "," + str(y_d) + "))"

        y_d = x[2] * tan(third_angle) * -1
        fourth_str = "l1 = Line(" + str(names_2) + ",(" + str(0) + "," + str(y_d) + "))"

        fith_str = str(name) + "_{1} = Intersect(l1, l)"
    sixth_str = f"Polygon({name}_{1}, {names_1}, {names_2})"
    return [first_str, second_str, third_str, fourth_str, fith_str, sixth_str]

if (int(second_angle != None) + int(first_angle != None) + int(third_angle != None)) == 2:
    if second_angle == None:
        second_angle = 2 * pi - first_angle - third_angle
    elif first_angle == None:
        first_angle = 2 * pi - second_angle - third_angle
    else:
        third_angle = 2 * pi - first_angle - second_angle

if (int(second_angle != None) + int(first_angle != None) + int(third_angle != None)) == 3:
    if first_segment != None:
        ans = izvesten_otrezok(names[0], first_segment, names[1], names[2], second_angle, third_angle, second_segment, third_segment)
    elif second_segment != None:
        ans = izvesten_otrezok(names[1], second_segment, names[0], names[2], first_angle, third_angle, first_segment, third_segment)
    elif third_segment != None:
        ans = izvesten_otrezok(names[2], third_segment, names[1], names[0], second_angle, first_angle, second_segment, first_segment)
    else:
        ans = izvesten_otrezok(names[0], first_segment, names[1], names[2], second_angle, third_angle, second_segment, third_segment)
elif (int(second_angle != None) + int(first_angle != None) + int(third_angle != None)) == 1:
    if first_angle != None:
        ans = izvesten_otrezok(names[1], second_segment, names[0], names[2], first_angle, third_angle, first_segment, third_segment)
    elif third_angle != None:
        ans = izvesten_otrezok(names[1], second_segment, names[0], names[2], first_angle, third_angle, first_segment, third_segment)
    elif second_angle != None:
        ans = izvesten_otrezok(names[2], third_segment, names[1], names[0], second_angle, first_angle, second_segment, first_segment)
elif (int(second_angle != None) + int(first_angle != None) + int(third_angle != None)) == 0:
    ans = izvesten_otrezok(names[1], second_segment, names[0], names[2], first_angle, third_angle, first_segment, third_segment)

import logging

geogebra_html_generator.insert_commands(ans)

