output_num = 7 
#number of output strings

def output_normalize(ret):
    objects = (text)
    output_text = ''
    for object_class in objects:
          output_text += (', '.join(object_class) + '\n')

def main_func(inp_str):
    #main func
    inp_str = string_split(inp_str)
    ret = assign_to_classes(inp_str)
    ret = list(ret)
    for i in range(output_num):
        ret[i] = str(ret[i])
    output_text = ''
    for object_class in ret:
          output_text += (''.join(object_class) + '\n')
        # if i < 6:
        #     ret[i] = ret[i][:] + "\n"
    return output_text #, sep="\n"

def string_split(inp_str):
    #creating list with diff objects
    inp_str = inp_str.split(",")
    return inp_str

def distillation(part):
    #highlithing the parts for final output
    new_part = ""
    for i in range(len(part)):
        try:
            if (46 < ord(part[i])< 58) or (64 < ord(part[i]) < 91) or (96 < ord(part[i]) < 123) or ord(part[i]) == 32:
                new_part = new_part[:] + str(part[i])            
        except:
            pass
    return new_part.strip()

def remarkable_point_processing(part):
    #smth for points
    if part.find("опис") != -1:
        part = part.replace("опис", "O")
    elif part.find("медиан") != -1:
        part = part.replace("медиан", "M")
    elif part.find("бисс") != -1:
        part = part.replace("бисс", "I")
    elif part.find("высот") != -1:
        part = part.replace("высот", "H")
    return part

def assign_to_classes(inp_str):
    polygons = []
    segments = []
    angles = []
    segments_relations = []
    angles_relations = []
    lines_intersection = []
    remarkable_points = []
    for part in inp_str:
        if part.find("угольн") != -1:
            polygons.append(distillation(part))
        elif part.find("отно") != -1 and (part.find("отр") != -1 or part.find("сторон") != -1):
            segments_relations.append(distillation(part))
        elif part.find("отно") != -1 and part.find("уг") != -1:
            angles_relations.append(distillation(part))
        elif part.find("отрез") != -1 or part.find("сторон") != -1 or part.find("диагонал") != -1:
            segments.append(distillation(part))
        elif part.find("перес") != -1:
            lines_intersection.append(distillation(part))
        elif part.find("уг") != -1:
            angles.append(distillation(part))
        elif part.find("опис") or (part.find("перес") and (part.find("медиан") != 3 or part.find("бисс") != -1 or part.find("высот") != -1)):
            part = remarkable_point_processing(part)
            remarkable_points.append(distillation(part))
    return polygons, segments, angles, segments_relations, angles_relations, lines_intersection, remarkable_points

inp = "треугольник ABC, угол ABC равен 30, сторона BC равна 10, угол BCA равен 40, сторона AB относится к BC как 5/3, S точка прересечения медиан ABC"
print(main_func(inp))

