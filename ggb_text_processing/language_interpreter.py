from re import *
# number of output strings = 8


def text_analyze(inp_str, output_num=7):
    """main function"""
    inp_str = inp_str.split("\n")
    statement = inp_str[0]
    question_existence = len(inp_str) > 1  # check question existence
    if question_existence:  # creat question if exist
        question = inp_str[1]

    statement = string_split(statement)
    ret = new_assign_to_classes(statement)
    ret = list(ret)

    if question_existence:  # analyze question if exist
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
    inp_str = sub(" и ",  ",", inp_str)
    inp_str = sub(r"([A-Z])(\s*=\s*)([A-Z, 0-9])", r"\1 = \3", inp_str)
    print(inp_str)
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
    part = distillation(part)
    part = sub(r"(^[A-Z]\s)([A-Z][A-Z]$)", r'\2 \1', part)
    return part


def summ_formatting(part):
    """new format for task_parser"""
    part = sub(r"([+-])([A-Z]+)", r"\2\1", part)
    return part


def distillation(part):
    """highlithing the parts for final output"""
    part = sub(r' [-]+ ', ' ', part)
    new_part = ""
    for i in range(len(part)):
        try:
            if ord(part[i]) == 42 or ord(part[i]) == 43 or (44 < ord(part[i]) < 58) or (64 < ord(part[i]) < 91) or ord(part[i]) == 32:  # without russian capitals
                new_part = new_part[:] + str(part[i])
        except Exception as exc:
            pass

    new_part = spaces_normalize(new_part)
    # new_part = output_formatting(new_part)
    return new_part.strip()


def equality_of_elem(part) -> str:
    """finding equal figures and transforming into output format"""
    part = sub(r'([A-Z, 0-9])(=)([A-Z, 0-9])', r'\1 = \3', part)
    if "равн" in part or "равен" in part:
        part = distillation(part)
        part = sub(r'([A-Z]{2,})(\s)([A-Z]{2,})', r'\1 = \3', part)
    part = sub(r"([A-Z][A-Z][A-Z])( = )([A-Z][A-Z][A-Z])", r'\1 \3 1/1', part)
    part = sub(r"([A-Z][A-Z])( = )([A-Z][A-Z])", r'\1 \3 1/1', part)
    return part


def algebraic_sum(part):
    """formatting sum and diff of angles and segments"""
    if "больш" in part:
        part = distillation(part)
        part = sub(r"(^[A-Z][A-Z])(\s)([A-Z][A-Z])", r"-\1 \3 ", part)
        part = sub(r"(^[A-Z][A-Z][A-Z])(\s)([A-Z][A-Z][A-Z])", r"-\1 \3 ", part)
    elif "меньш" in part:
        part = distillation(part)
        part = sub(r"(^[A-Z][A-Z])(\s)([A-Z][A-Z])", r"-\3 \1 ", part)
        part = sub(r"(^[A-Z][A-Z][A-Z])(\s)([A-Z][A-Z][A-Z])", r"-\3 \1 ", part)
    elif "сумм" in part:
        part = distillation(part)
        part = sub(r"(^[A-Z][A-Z])(\s)([A-Z][A-Z])", r"+\1 \3 ", part)
        part = sub(r"(^[A-Z][A-Z][A-Z])(\s)([A-Z][A-Z][A-Z])", r"+\1 \3 ", part)
    return part


def within_polygon(part):
    """formatting points within polygon"""
    if "леж" in part or "внутр" in part or "наход" in part:
        part = distillation(part)
        part = sub(r"(^[A-Z])(\s)([A-Z]+)$", r"\1 /// \3", part)
        part = sub(r"([A-Z]{2,})(\s)([A-Z])$", r"\3 /// \1", part)
        # part = sub(r"([A-Z]+)(\s)([A-Z])(\s)", r"\3 * \1", part)
    return part


def remarkable_point_processing(part):
    """remarkable points parcing"""
    if "опис" in part:
        part = sub("опис", "O", part)
        # part = part.replace("опис", "O")
    elif "медиан" in part or "центроид" in part:
        part = sub("центроид", "M", part)
        part = sub("медиан", "M", part)
        # part = part.replace("медиан", "M")
    elif "бисс" in part or "инцентр" in part or "впис" in part:
        part = sub("инцентр", "I", part)
        part = sub("впис", "I", part)
        part = sub("бисс", "I", part)
        # part = part.replace("бисс", "I")
    elif "высот" in part or "ортоцен" in part:
        part = sub("ортоцен", "H", part)
        part = sub("высот", "H", part)
        # part = part.replace("высот", "H")
    return part


def class_analyze(part):
    """analyzing to which class this part belong"""

    poly = False
    if "угольн" in part or "подоб" in part:
        poly = True

    if "больш" in part or "меньш" in part or "сумм" in part:
        part = algebraic_sum(part)

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
        elif ord(object[0]) == 43 or ord(object[0]) == 45:
            if len(object) == 3:
                segments_parts += 1
            elif len(object) == 4:
                let_parts += 1
        elif 44 < ord(object[0]) < 59:
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
        part = algebraic_sum(part)
        part = equality_of_elem(part)
        if cla == "polygon":
            part = sub("невыпукл", "*", part)
            polygons.append(distillation(part))
        elif cla == "segment_rel":
            part = summ_formatting(part)
            part = output_formatting(part)
            segments_relations.append(distillation(part))
        elif cla == "angle_rel":
            part = summ_formatting(part)
            angles_relations.append(distillation(part))
        elif cla == "rem_point":
            part = within_polygon(part)
            part = remarkable_point_processing(part)
            part = distillation(part)
            part = sub("///", "in", part)
            polygons.append(part)
        elif cla == "segment":
            segments.append(distillation(part))
        elif cla == "lines_intersection":
            lines_intersection.append(distillation(part))
        elif cla == "angle":
            angles.append(distillation(part))
        elif cla == "polygon_rel":
            polygon_relation.append(distillation(part))

    # print(segments_relations)
    return polygons, segments, angles, segments_relations, angles_relations, polygon_relation, lines_intersection


def question_processing(question):
    """putting a question in the output format"""
    poly = False
    if "угольн" in question or "подоб" in question:
        poly = True
    question = equality_of_elem(question)
    if poly:
        question = distillation(question)
        question = sub(r"(^\w+)(\s)(\w*)(\s)(\d)", r'/\1 \3 \5', question)
        question = sub(r"(^\w+)(\s*)(\w*$)", r'/\1 \3 ?', question)
    elif "больш" in question or "меньш" in question or "сумм" in question:
        question = algebraic_sum(question)
        question = sub(r"([A-Z])(\s*)$", r"\1 ?", question)
        question = summ_formatting(question)
    else:
        question = distillation(question)
        question = sub(r"(^\w+)(\s)(\w*)(\s)(\d+)", r'\1 \3 \5', question)
        question = sub(r"(^\w+)(\s*)(\w*$)", r'\1 \3 ?', question)
    return question
