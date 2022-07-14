#number of output strings = 7

def text_analyze(inp_str, output_num=6):
    """main func"""
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
    """creating list with diff objects"""
    inp_str = inp_str.split(",")
    return inp_str


def distillation(part):
    """highlithing the parts for final output"""
    new_part = ""
    for i in range(len(part)):
        try:
            if (45 < ord(part[i])< 58) or (64 < ord(part[i]) < 91) or (96 < ord(part[i]) < 123) or ord(part[i]) == 32:
                new_part = new_part[:] + str(part[i])            
        except:
            pass
    return new_part.strip()


def remarkable_point_processing(part):
    """smth for points"""
    if "опис" in part:
        part = part.replace("опис", "O")
    elif "медиан" in part:
        part = part.replace("медиан", "M")
    elif "бисс" in part:
        part = part.replace("бисс", "I")
    elif "высот" in part:
        part = part.replace("высот", "H")
    return part


def assign_to_classes(inp_str):
    polygons = []
    segments = []
    angles = []
    segments_relations = []
    angles_relations = []
    lines_intersection = []

    for part in inp_str:
        if "угольн" in part:
            polygons.append(distillation(part))
        elif "отно" in part and ("отр" in part or "сторон" in part):
            segments_relations.append(distillation(part))
        elif "отно" in part and "уг" in part:
            angles_relations.append(distillation(part))
        elif "опис" in part or (("перес" in part  and (("медиан" in part or "бисс" in part or "высот" in part)))):
            part = remarkable_point_processing(part)
            polygons.append(distillation(part))
        elif "отрез" in part or "сторон" in part or "диагонал" in part:
            segments.append(distillation(part))
        elif "перес" in part:
            lines_intersection.append(distillation(part))
        elif "уг" in part:
            angles.append(distillation(part))
    return polygons, segments, angles, segments_relations, angles_relations, lines_intersection

inp = 'треугольник ABC, сторона AB = 5, сторона BC = 4, сторона AB относится к AC как 5/3, угол ACB равен 90, I точка пересечения биссектрисс в ABC'
print(text_analyze(inp))

