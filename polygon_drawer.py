import geogebra_html_generator
import triangle_drawer
import task_parser as taskp


# отрисовка треугольника по именам вершин
def triangle_from_task_drawer(A, B, C):
    
    AB = taskp.find_segment_with_points(A, B).size
    BC = taskp.find_segment_with_points(B, C).size
    CA = taskp.find_segment_with_points(C, A).size
    
    sides = [BC, CA, AB]
    
    CBA = taskp.find_angle_with_points(C, B, A).size
    ACB = taskp.find_angle_with_points(A, C, B).size
    BAC = taskp.find_angle_with_points(B, A, C).size
    
    angles, angles_names = [BAC, CBA, ACB], [f"{B}{A}{C}", f"{C}{B}{A}", f"{A}{C}{B}"]
    
    triangle_drawer.DrawTriangle(triangle_drawer.CreateTriangle(sides, angles, angles_names))
    
    
# Волчкевич страница 26 задача 1
text1 = 'ABC'  # многоугольники
text2 = 'AC 4'  # дополнительные отрезки
text3 = ''  # углы по трем точкам или между прямыми
text4 = ''  # отношения отрезков
text5 = ''  # отношения углов
text6 = ''  # точки пересечения прямых

taskp.polygons_create(text1)
taskp.segments_create(text2)
taskp.angles_create(text3)
taskp.segments_relations_create(text4)
taskp.angles_relations_create(text5)
taskp.line_intersection_create(text6)

triangle_from_task_drawer(taskp.polygons[0].points[0].name, taskp.polygons[0].points[1].name, taskp.polygons[0].points[2].name)
