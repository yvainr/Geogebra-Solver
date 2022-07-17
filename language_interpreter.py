#number of output strings = 6

def text_analyze(inp_str, output_num=6):
    """main function"""
    inp_str = string_split(inp_str)
    ret = new_assign_to_classes(inp_str)
    ret = list(ret)
    for i in range(output_num):
        ret[i] = str(ret[i])
    output_text = ''
    for object_class in ret:
        output_text += (''.join(object_class) + '\n')

    return output_text


def string_split(inp_str):
    """creating list with diff objects"""
    inp_str = inp_str.split(",")
    return inp_str


def spaces_normalize(part):
    """deleting extra spaces"""
    part = part.split()
    n_part = ''
    for word in part:
        n_part += word
        n_part += " "
    return n_part


def distillation(part):
    """highlithing the parts for final output"""
    new_part = ""
    for i in range(len(part)):
        try:
            if (45 < ord(part[i])< 58) or (64 < ord(part[i]) < 91) or (96 < ord(part[i]) < 123) or ord(part[i]) == 32:
                new_part = new_part[:] + str(part[i])
        except:
            pass
    new_part = spaces_normalize(new_part)
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


def class_analyze(part):
    """analyzing to which class this part belong"""
    part = part.split()
    points_parts = 0
    segments_parts = 0
    let_parts = 0
    num_parts = 0
    for object in part:
        if 64 < ord(object[0]) < 91:
            if len(object) == 1:
                points_parts += 1
            elif len(object) == 2:
                segments_parts += 1
            elif len(object) > 2:
                let_parts += 1
        elif 45 < ord(object[0]) < 59:
            num_parts += 1
    ret = "polygon"
    if let_parts == 1 and points_parts == 0 and segments_parts == 0 and num_parts == 0:
        ret = "polygon"
    elif let_parts == 0 and points_parts == 0 and segments_parts == 1 and num_parts == 1:
        ret = "segment"
    elif let_parts == 1 and points_parts == 0 and segments_parts == 0 and num_parts == 1:
        ret = "angle"
    elif let_parts == 2 and points_parts == 0 and segments_parts == 0 and num_parts == 1:
        ret = "angle_rel"
    elif let_parts == 0 and points_parts == 0 and segments_parts == 2 and num_parts == 1:
        ret = "segment_rel"
    elif let_parts == 0 and points_parts == 1 and segments_parts == 2 and num_parts == 0:
        ret = "lines_intersection"
    elif let_parts == 1 and points_parts == 1 and segments_parts == 0 and num_parts == 0:
        ret = "rem_point"

    return ret


def new_assign_to_classes(inp_str):
    polygons = []
    segments = []
    angles = []
    segments_relations = []
    angles_relations = []
    lines_intersection = []

    for part in inp_str:
        cla = class_analyze(part)
        if cla == "polygon":
            polygons.append(distillation(part))
        elif cla == "segment_rel":
            segments_relations.append(distillation(part))
        elif cla == "angle_rel":
            angles_relations.append(distillation(part))
        elif cla == "rem_point":
            part = remarkable_point_processing(part)
            polygons.append(distillation(part))
        elif cla == "segment":
            segments.append(distillation(part))
        elif cla == "lines_intersection":
            lines_intersection.append(distillation(part))
        elif cla == "angle":
            angles.append(distillation(part))

    return polygons, segments, angles, segments_relations, angles_relations, lines_intersection

inp = 'треугольник ABC, AB = 5, сторона BC = 4.5, AB относится к AC как 5/3,  ACB равен 90, I точка пересечения биссектрисс в ABC'
print(text_analyze(inp))
