output_num = 6 
#number of output strings

def main_func(inp_str):
    #main func
    inp_str = string_split(inp_str)
    ret = assign_to_classes(inp_str)
    return ret #, sep="\n"

def string_split(inp_str):
    #creating list with diff objects
    inp_str = inp_str.split(",")
    return inp_str

def distillation(part):
    #highlithing the parts for final output
    new_part = ""
    for i in range(len(part)):
        try:
            if (47 < ord(part[i])< 58) or (64 < ord(part[i]) < 91) or (96 < ord(part[i]) < 123) or ord(part[i]) == 32:
                new_part = new_part[:] + str(part[i])            
        except:
            pass
    return new_part.strip()

def assign_to_classes(inp_str):
    polygons = []
    segments = []
    angles = []
    segments_relations = []
    angles_relations = []
    lines_intersection = []
    for part in inp_str:
        if part.find("угольн") != -1:
            polygons.append(distillation(part))
        elif part.find("отрез") + part.find("сторон") + part.find("диагонал") > -3:
            segments.append(distillation(part))
        elif part.find("отно") != -1 and part.find("отр") != -1:
            segments_relations.append(distillation(part))
        elif part.find("отно") != -1 and part.find("уг") != -1:
            angles_relations.append(distillation(part))
        elif part.find("перес") != -1:
            lines_intersection.append(distillation(part))
        elif part.find("уг") != -1:
            angles.append(distillation(part))
    return polygons, segments, angles, segments_relations, angles_relations, lines_intersection

inp = "треугольник ABC, угол ABC равен 30, сторона BC равна 10"
print(main_func(inp))

