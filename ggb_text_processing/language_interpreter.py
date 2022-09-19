from re import *
# number of output strings = 2


def text_analyze(inp_str):
    """main function"""
    inp_str = inp_str.split("\n")
    statement = inp_str[0]
    question_existence = len(inp_str) > 1  # check question existence
    if question_existence:  # creat question if exist
        questions = inp_str[1]

    statement = string_split(statement)
    ret = fresh_assign_to_classes(statement)
    ret = list(ret)
    que_ret = list()

    if question_existence:  # analyze question if exist
        questions = questions.split(",")
        new_questions = list()
        for question in questions:
            new_questions.append(question_processing(question))
        que_ret.append(new_questions)

    output_text = ''
    for object_class in ret:
        output_text += object_class + ", "
    output_text = output_text[:-2]
    output_text += '\n'
    for question_class in que_ret:
        question_class = str(question_class)
        if "[" in question_class:
            output_text += (', '.join(list(eval(question_class))))
        else:
            output_text += question_class
    return output_text


def string_split(inp_str):
    """creating list with diff objects"""
    inp_str = sub(r"([A-Z])(\s*=\s*)([A-Z, 0-9])", r"\1 = \3", inp_str)
    inp_str = inp_str.split(",")
    for part in inp_str:
        if " и " in part and not ("отношени" in part or "сумм" in part or "относ" in part):
            n_part = sub(" и ", ",", part)
            n_part = n_part.split(",")
            inp_str.remove(part)
            for item in n_part:
                inp_str.append(item)
    return inp_str


def spaces_normalize(part) -> str:
    """deleting extra spaces"""
    part = part.split()
    new_part = ''
    for word in part:
        new_part += word
        new_part += " "
    return new_part


def segment_rel_formatting(part) -> str:
    """putting segment relation in correct order"""
    part = distillation(part)
    part = sub(r"(^[A-Z]\s)([A-Z][A-Z])(\s)", r'\2 \1', part)
    return part


def summ_formatting(part) -> str:
    """new format for task_parser"""
    part = sub(r"([+-])([A-Z]+)", r"\2\1", part)
    return part


def distillation(part) -> str:
    """highlithing the parts for final output"""
    part = sub(r' [-]+ ', ' ', part)
    new_part = ""
    for i in range(len(part)):
        try:
            if ord(part[i]) == 42 or ord(part[i]) == 43 or (44 < ord(part[i]) < 58) or (64 < ord(part[i]) < 91) or ord(part[i]) == 32 or ord(part[i]) == 124:  # without russian capitals
                new_part = new_part[:] + str(part[i])
        except:
            pass

    new_part = spaces_normalize(new_part)
    return new_part.strip()


def ang_distillation(part) -> str:
    """special distillation for angles func"""
    new_part = ""
    for i in range(len(part)):
        try:
            if ord(part[i]) == 42 or ord(part[i]) == 43 or (44 < ord(part[i]) < 58) or (64 < ord(part[i]) < 91) or ord(
                    part[i]) == 32 or ord(part[i]) == 1074:  # without russian capitals
                new_part = new_part[:] + str(part[i])
        except:
            pass

    new_part = spaces_normalize(new_part)
    return new_part.strip()


def eq_distillation(part):
    """highlighting the parts for equality function"""
    part = sub(r' [-]+ ', ' ', part)
    new_part = ""
    for i in range(len(part)):
        try:
            if ord(part[i]) == 61 or ord(part[i]) == 43 or (44 < ord(part[i]) < 58) or (64 < ord(part[i]) < 91) or ord(part[i]) == 32:  # without russian capitals
                new_part = new_part[:] + str(part[i])
        except Exception as exc:
            pass

    new_part = spaces_normalize(new_part)
    return new_part.strip()


def equality_of_elem(part) -> str:
    """finding equal figures and transforming into output format"""
    if ("равн" in part or "равен" in part) and "сумм" not in part and "отношен" not in part:
        part = distillation(part)
        part = sub(r'([A-Z]{2,})(\s)([A-Z]{2,})', r'\1 = \3', part)
    if "=" in part:
        part = sub(r'(\s*)( = )(\s*)', r'\2', part)
        part = eq_distillation(part)
        part = sub(r"([A-Z][A-Z][A-Z])( = )([A-Z][A-Z][A-Z])", r'\1 \3 1/1', part)
        part = sub(r"([A-Z][A-Z])( = )([A-Z][A-Z])", r'\1 \3 1/1', part)
    return part


def algebraic_sum(part) -> str:
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


def element_formatting(part, cla):
    """putting element in output format"""
    if cla == "ray":
        part = sub(r'([A-Z][A-Z])', r'|\1', part)
    elif cla == "line":
        part = sub(r'([A-Z][A-Z])', r'/\1', part)
    elif cla == "polygon":
        part = sub(r'([A-Z]{3,})', r'/\1', part)
    elif cla == "polygon_rel":
        part = sub(r'(^[A-Z])', r'/\1', part)
    return part


def within_polygon(part) -> str:
    """formatting points within polygon"""
    if "леж" in part or "внутр" in part or "наход" in part:
        part = distillation(part)
        part = sub(r"(^[A-Z])(\s)([A-Z]{2,})$", r"\1 /// \3", part)
        part = sub(r"([A-Z]{2,})(\s)([A-Z])$", r"\3 /// \1", part)
        # part = sub(r"([A-Z]+)(\s)([A-Z])(\s)", r"\3 * \1", part)
    return part


def points_on_line(part) -> str:
    """processing points on line"""
    if "на" in part and "прямой" in part:
        part = distillation(part)
        part = sub(r"^([A-Z])(\s)([A-Z]?)(\s?)([A-Z]?(\s?)([A-Z]*))", r"(\1 \3 \5 /// \7)", part)
    return part


def nested_angles(part) -> str:
    """formatting angles embedded in each other"""
    if "в" in part and "угл" in part:
        part = ang_distillation(part)
        part = sub(r"([A-Z][A-Z][A-Z])(\s)(в)(\s)([A-Z][A-Z][A-Z])", r"\1 /// \5", part)
        part = sub(r"(в)([A-Z][A-Z][A-Z])(\s)([A-Z][A-Z][A-Z])", r"\4 /// \2", part)
    return part


def ray_within_angle(part) -> str:
    """formatting ray within angle"""
    if "в" in part and "луч" in part and "уг" in part:
        part = distillation(part)
        part = sub(r"(^[A-Z][A-Z])(\s)([A-Z][A-Z][A-Z])$", r"\1 /// \3", part)
        part = sub(r"(^[A-Z][A-Z][A-Z])(\s)([A-Z][A-Z])$", r"\3 /// \1", part)
    return part


def points_on_element(part) -> str:
    """processing point on line, ray or segment"""
    part = distillation(part)
    part = sub(r"^([A-Z])(\s)([A-Z][A-Z])", r"\1 /// \3", part)
    part = sub(r"^([A-Z][A-Z])(\s)([A-Z])$", r"\3 /// \1", part)
    return part


def point_on_line(part) -> str:
    """processing point on line"""
    part = distillation(part)
    part = sub(r"^([A-Z])(\s)([A-Z][A-Z])", r"\1 /// /\3", part)
    part = sub(r"^([A-Z][A-Z])(\s)([A-Z])$", r"/\3 /// \1", part)
    return part


def point_on_ray(part) -> str:
    """processing point on ray"""
    part = distillation(part)
    part = sub(r"^([A-Z])(\s)([A-Z][A-Z])", r"\1 /// |\3", part)
    part = sub(r"^([A-Z][A-Z])(\s)([A-Z])$", r"|\3 /// \1", part)
    return part


def remarkable_lines(part, triangle="") -> str:
    """medians, bisectors and altitudes processing"""
    if "медиан" in part:
        part = distillation(part)
        # part = sub(r'(^[A-Z][A-Z])(\s)', r'\1 M ', part)
        part = part[:] + " M " + triangle
    elif "бисс" in part:
        part = distillation(part)
        # part = sub(r'(^[A-Z][A-Z])(\s)', r'\1 I', part)
        part = part[:] + " I " + triangle
    elif "высот" in part:
        part = distillation(part)
        # part = sub(r'(^[A-Z][A-Z])(\s)', r'\1 H', part)
        part = part[:] + " H " + triangle
    return part


def remarkable_point_processing(part) -> str:
    """remarkable points parcing"""
    if "опис" in part:
        part = sub("опис", "O", part)
    elif ("центр" in part and "медиан" in part) or "центроид" in part:
        part = sub("центроид", "M", part)
        part = sub("медиан", "M", part)
    elif ("центр" in part and "бисс" in part) or "инцентр" in part or "впис" in part:
        part = sub("инцентр", "I", part)
        part = sub("впис", "I", part)
        part = sub("бисс", "I", part)
    elif ("центр" in part and "высот" in part) or "ортоцен" in part:
        part = sub("ортоцен", "H", part)
        part = sub("высот", "H", part)
    return part


def class_analyze(part) -> str:
    """analyzing to which class this part belong"""

    part = sub(chr(9651), "треугольник ", part)
    part = sub(chr(8736), "угол ", part)
    if "больш" in part or "меньш" in part or "сумм" in part:
        part = algebraic_sum(part)
    context = part
    part = equality_of_elem(part)
    part = part.split()
    points_parts = 0
    segments_parts = 0
    polygons_parts = 0
    angle_parts = 0
    ray_parts = 0
    line_parts = 0
    rem_lines = 0
    num_parts = 0
    for objec in part:
        if 64 < ord(objec[0]) < 91:
            if len(objec) == 1:
                points_parts += 1
            elif len(objec) == 2:
                if "луч" in context:
                    ray_parts += 1
                elif "прям" in context or "лини" in context:
                    line_parts += 1
                elif "медиан" in context or "бисс" in context or "высот" in context:
                    rem_lines += 1
                else:
                    segments_parts += 1
            elif len(objec) == 3:
                if "угольн" in context or "подоб" in context:
                    polygons_parts += 1
                else:
                    angle_parts += 1
            else:
                polygons_parts += 1
        elif ord(objec[0]) == 43 or ord(objec[0]) == 45:
            if len(objec) == 3:
                segments_parts += 1
            elif len(objec) == 4:
                angle_parts += 1
        elif 44 < ord(objec[0]) < 59:
            num_parts += 1

    ret = "polygon"

    if points_parts == 0 and segments_parts == 0 and ray_parts == 0 and line_parts == 0 and angle_parts == 0 and polygons_parts == 1 and num_parts == 0:
        ret = "polygon"
    elif points_parts == 0 and segments_parts == 1 and ray_parts == 0 and line_parts == 0 and angle_parts == 0 and polygons_parts == 0 and num_parts == 1:
        ret = "segment"
    elif points_parts == 0 and segments_parts == 1 and ray_parts == 0 and line_parts == 0 and angle_parts == 0 and polygons_parts == 0 and num_parts == 0:
        ret = "simple_segment"
    elif points_parts == 0 and segments_parts == 0 and ray_parts == 1 and line_parts == 0 and angle_parts == 0 and polygons_parts == 0 and num_parts == 0:
        ret = "ray"
    elif points_parts == 0 and segments_parts == 0 and ray_parts == 0 and line_parts == 1 and angle_parts == 0 and polygons_parts == 0 and num_parts == 0:
        ret = "line"
    elif points_parts == 0 and segments_parts == 0 and ray_parts == 0 and line_parts == 0 and angle_parts == 1 and polygons_parts == 0 and num_parts == 1:
        ret = "angle"
    elif points_parts == 0 and segments_parts == 0 and ray_parts == 0 and line_parts == 0 and angle_parts == 0 and polygons_parts == 2 and num_parts == 1:
        ret = "polygon_rel"
    elif points_parts == 0 and segments_parts == 0 and ray_parts == 0 and line_parts == 0 and angle_parts == 2 and polygons_parts == 0 and num_parts == 1:
        ret = "angle_rel"
    elif points_parts == 1 and segments_parts == 1 and ray_parts == 0 and line_parts == 0 and angle_parts == 0 and polygons_parts == 0 and num_parts == 1:
        ret = "point_segment_rel"
    elif points_parts == 0 and segments_parts == 2 and ray_parts == 0 and line_parts == 0 and angle_parts == 0 and polygons_parts == 0 and num_parts == 1:
        ret = "segment_rel"
    elif points_parts == 1 and segments_parts == 0 and ray_parts == 0 and line_parts == 2 and angle_parts == 0 and polygons_parts == 0 and num_parts == 0:
        ret = "lines_intersection"
    elif points_parts == 1 and segments_parts == 0 and ray_parts == 0 and line_parts == 0 and angle_parts == 0 and polygons_parts == 1 and num_parts == 0:
        ret = "rem_point"
    elif points_parts == 1 and segments_parts == 1 and ray_parts == 0 and line_parts == 0 and angle_parts == 0 and polygons_parts == 0 and num_parts == 0:
        ret = "point_on_seg"
    elif points_parts == 1 and segments_parts == 0 and ray_parts == 0 and line_parts == 1 and angle_parts == 0 and polygons_parts == 0 and num_parts == 0:
        ret = "point_on_line"
    elif points_parts == 1 and segments_parts == 0 and ray_parts == 1 and line_parts == 0 and angle_parts == 0 and polygons_parts == 0 and num_parts == 0:
        ret = "point_on_ray"
    elif points_parts == 0 and segments_parts == 1 and ray_parts == 0 and line_parts == 0 and angle_parts == 2 and polygons_parts == 0 and num_parts == 0:
        ret = "angle_in_angle"
    elif points_parts == 0 and segments_parts == 0 and ray_parts == 1 and line_parts == 0 and angle_parts == 1 and polygons_parts == 0 and num_parts == 0:
        ret = "ray_in_angle"
    elif rem_lines == 1:
        ret = "rem_lines"

    return ret


def fresh_assign_to_classes(inp_str):
    polygons = []
    # segments = []
    # lines = []
    # rays = []
    # angles = []
    # segments_relations = []
    # angles_relations = []
    # polygon_relation = []
    # lines_intersection = []
    # points_on_segment = []
    # points_on_lines = []
    # points_on_ray = []
    # angle_in_angle = []
    # rays_in_angle = []
    # rem_lines = []
    # points_on_straight = []
    # points_in_polygon = []
    # point_segment_relation = []
    output = []

    polygon_num = 0

    for part in inp_str:
        cla = class_analyze(part)
        part = algebraic_sum(part)
        part = equality_of_elem(part)
        # part = element_formatting(part, cla)
        if cla == "polygon":
            part = sub("невыпукл", "*", part)
            part = distillation(part)
            polygons.append(part)
            part = "poly " + part[:]
            output.append(part)
            polygon_num += 1
        elif cla == "simple_segment":
            part = distillation(part)
            part = "poly " + part[:]
            output.append(part)
        elif cla == "segment":
            part = distillation(part)
            part = "seg " + part[:]
            output.append(part)
        elif cla == "angle":
            part = distillation(part)
            part = "ang " + part[:]
            output.append(part)
        elif cla == "segment_rel":
            part = summ_formatting(part)
            part = distillation(part)
            part = "seg_rel " + part[:]
            output.append(part)
        elif cla == "angle_rel":
            part = summ_formatting(part)
            part = distillation(part)
            part = "ang_rel " + part[:]
            output.append(part)
        elif cla == "polygon_rel":
            part = element_formatting(part, cla)
            part = distillation(part)
            part = "poly_rel " + part[:]
            output.append(part)
        elif cla == "lines_intersection":
            part = distillation(part)
            part = "lin_int " + part[:]
            output.append(part)
        elif cla == "point_on_seg":
            part = points_on_element(part)
            part = distillation(part)
            part = sub("///", "in", part)
            part = "p_str " + part[:]
            output.append(part)
        elif cla == "point_on_ray":
            part = point_on_ray(part)
            part = distillation(part)
            part = sub("///", "in", part)
            part = "p_str " + part[:]
            output.append(part)
        elif cla == "point_on_line":
            part = point_on_line(part)
            part = distillation(part)
            part = sub("///", "in", part)
            part = "p_str " + part[:]
            output.append(part)
        elif cla == "rem_point":
            part = within_polygon(part)
            part = remarkable_point_processing(part)
            part = distillation(part)
            part = sub("///", "in", part)
            part = "p_poly " + part[:]
            output.append(part)
        elif cla == "point_segment_rel":
            part = segment_rel_formatting(part)
            part = "p_seg_rel " + part[:]
            output.append(part)
        elif cla == "line":
            output.append(distillation(part))
        elif cla == "ray":
            output.append(distillation(part))
        elif cla == "angle_in_angle":
            part = nested_angles(part)
            part = distillation(part)
            part = sub("///", "in", part)
            output.append(part)
        elif cla == "ray_in_angle":
            part = ray_within_angle(part)
            part = distillation(part)
            part = sub("///", "in", part)
            output.append(part)
        elif cla == "rem_lines":
            triangle = ""
            if polygon_num == 1:
                triangle = polygons[0]
            elif polygon_num > 1:
                name = search(r'[A-Z]{2}', part)
                name = name.group()
                for poly in polygons:
                    if len(list(set(name) & set(poly))) == 1:
                        triangle = poly
                        break

            part = remarkable_lines(part, triangle)
            output.append(distillation(part))
        # print(part)
    return output  # polygons, segments, angles, segments_relations, angles_relations, polygon_relation, lines_intersection, points_on_straight, points_in_polygon, point_segment_relation -- angle_in_angle, rays_in_angle, rem_lines


def question_processing(question) -> str:
    """putting a question in the output format"""
    question = sub(chr(9651), "треугольник ", question)
    question = sub(chr(8736), "угол ", question)
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
