# import drawer_ggb.geogebra_html_generator as geogebra_html_generator
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

def text_splitter(text):
    taskp.points.clear()
    taskp.lines.clear()
    taskp.angles.clear()
    taskp.segments.clear()
    taskp.polygons.clear()

    text = text.replace('\r', '').split('\n')
    print(text)
    try:
        taskp.polygons_create(text[0])
        taskp.segments_create(text[1])
        taskp.angles_create(text[2])
        taskp.segments_relations_create(text[3])
        taskp.angles_relations_create(text[4])
        taskp.line_intersection_create(text[5])
    except IndexError:
        pass

    triangle_from_task_drawer(taskp.polygons[0].points[0].name, taskp.polygons[0].points[1].name, taskp.polygons[0].points[2].name)


