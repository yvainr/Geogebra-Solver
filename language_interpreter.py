from re import *
#number of output strings = 8

def text_analyze(inp_str, output_num=7):
    """main function"""
    inp_str = inp_str.split("\n")
    statement = inp_str[0]
    try:
        question = inp_str[1]
    except:
        question = ""
    statement = string_split(statement)
    ret = new_assign_to_classes(statement)
    ret = list(ret)
    ret.append(question_processing(question))
    for i in range(output_num):
        ret[i] = str(ret[i])
    output_text = ''
    for object_class in ret:
        if "[" in object_class:
            output_text += (', '.join(list(eval(object_class))) + '\n')
        else:
            output_text += object_class

    return output_text


def string_split(inp_str):
    """creating list with diff objects"""
    inp_str = inp_str.split(",")
    return inp_str


def spaces_normalize(part):
    """deleting extra spaces"""
    part = part.split()
    new_part = ''
    for word in part:
        new_part += word
        new_part += " "
    return new_part


def output_formatting(part):
    """putting segment relation in correct order"""
    part = sub(r"(^[A-Z]\s)([A-Z][A-Z])", r'\2 \1', part)
    return part


def distillation(part):
    """highlithing the parts for final output"""
    new_part = ""
    for i in range(len(part)):
        try:
            if ord(part[i]) == 42 or (45 < ord(part[i])< 58) or (64 < ord(part[i]) < 91) or ord(part[i]) == 32:
                new_part = new_part[:] + str(part[i])
        except:
            pass
    new_part = spaces_normalize(new_part)
    new_part = output_formatting(new_part)
    return new_part.strip()


def equality_of_elem(part):
    """finding equal figures and transforming into output format""" 
    part = sub(r"([A-Z][A-Z][A-Z])( = )([A-Z][A-Z][A-Z])", r'\1 \3 1/1', part)
    part = sub(r"([A-Z][A-Z])( = )([A-Z][A-Z])", r'\1 \3 1/1', part)
    return part


def remarkable_point_processing(part):
    """smth for points"""
    if "опис" in part:
        part = part.replace("опис", "O")
    elif "медиан" in part or "центроид" in part:
        part = sub("центроид", "медиан", part)
        part = part.replace("медиан", "M")
    elif "бисс" in part or "инцентр" in part or "впис" in part:
        part = sub("инцентр", "бисс", part)
        part = sub("впис", "бисс", part)
        part = part.replace("бисс", "I")
    elif "высот" in part or "ортоцен" in part:
        part = sub("ортоцен", "высот", part)
        part = part.replace("высот", "H")
    return part


def class_analyze(part):
    """analyzing to which class this part belong"""

    poly = False
    if "угольн" in part or "подоб" in part:
        poly = True

    part = equality_of_elem(part)
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
    elif let_parts == 2 and points_parts == 0 and segments_parts == 0 and num_parts == 1 and poly:
        ret = "polygon_rel"
    elif let_parts == 2 and points_parts == 0 and segments_parts == 0 and num_parts == 1:
        ret = "angle_rel"
    elif let_parts == 0 and points_parts == 1 and segments_parts == 1 and num_parts == 1:
        ret = "segment_rel"
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
    polygon_relation = []
    lines_intersection = []

    for part in inp_str:
        cla = class_analyze(part)
        part = equality_of_elem(part)
        if cla == "polygon":
            part = sub("невыпукл", "*", part)
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
        elif cla == "polygon_rel":
            polygon_relation.append(distillation(part))

    return polygons, segments, angles, segments_relations, angles_relations, polygon_relation, lines_intersection


def question_processing(question):
    """putting a question in the output format"""
    poly = False
    if "угольн" in question or "подоб" in question:
        poly = True
    question = equality_of_elem(question)
    question = distillation(question)
    if poly:
        question = sub(r"(^\w+)(\s)(\w*)(\s)(\d)", r'/\1 \3 \5', question)
        question = sub(r"(^\w+)(\s)(\w*$)", r'/\1 \3 ?', question)
    else:
        question = sub(r"(^\w+)(\s)(\w*)(\s)(\d+)", r'\1 \3 \5', question)
        question = sub(r"(^\w+)(\s)(\w*$)", r'\1 \3 ?', question)
    return question


inpu = 'ABC, DEF, ABC подобен DEF с коэффициентом 1/2, relation of sides AB and BC is 1/2'
inp = 'треугольники ABC = HFG, ABCD невыпуклый, AB = 5, сторона BC равна 4, AB = AC,  ACB равен 90, I инцентр в ABC, точкой M сторона AB делится в отношении 1/2 \n доказать что подобны ABC DEF 1/2'
print(text_analyze(inp))


