import task_parser as taskp


def fact_objects_name(fact):
    """importing needed attributes from class"""
    names = []
    for item in fact.objects:
        naming = ""
        if isinstance(item, taskp.Segment):
            for point in item.points:
                naming += point.name
        elif isinstance(item, taskp.Angle):
            for ray in item.rays:
                naming += ray.main_point.name
                naming += (list(ray.points))[0].name
            naming = naming[1:]
        elif isinstance(item, taskp.Point):
            naming += item.name
        elif isinstance(item, taskp.Line):
            naming += (list(item.points))[0].name
            naming += (list(item.points))[1].name
        elif isinstance(item, taskp.Polygon):
            for point in item.points:
                naming += point.name
        elif isinstance(item, taskp.Ray):
            naming += ray.main_point.name
            naming += (list(ray.points))[0].name
        names.append(naming)
    return names


def angle_formalization(fact):
    """adding angle signs"""
    angle = False
    for item in fact.objects:
        if isinstance(item, taskp.Angle) and fact.value is not None:
            angle = True
    return angle


def fact_output(fact):
    """main func: collecting data for output and choosing template"""
    try:
        equality = False
        relation = False
        size = False
        diff = False
        add = False
        value = fact.value
        if fact.fact_type == "relation":
            if value == "1/1" or value == 1.0:
                equality = True
            else:
                relation = True
        elif fact.fact_type == "size":
            size = True
        elif fact.fact_type == "difference":
            diff = True
        elif fact.fact_type == "addition":
            add = True

        names = fact_objects_name(fact)
        question = False
        if value is None:
            question = True
            value = "?"

        name1 = names[0]
        ang_sign = u"\u2220"
        deg_sign = u"\N{DEGREE SIGN}"

        if size:
            return f'{ang_sign if angle_formalization(fact) else ""}{name1} = {value if question else value.conversion_to_latex()}{deg_sign if angle_formalization(fact) else ""}'
        else:
            name2 = names[1]
            if equality:
                return f'{ang_sign if angle_formalization(fact) else ""}{name1} = {ang_sign if angle_formalization(fact) else ""}{name2}'
            elif relation:
                return f'{ang_sign if angle_formalization(fact) else ""}{name1}/{ang_sign if angle_formalization(fact) else ""}{name2} = {value if question else value.conversion_to_latex()}'
            elif diff:
                if len(fact.objects) == 3:
                    name3 = names[2]
                    return f'{ang_sign if angle_formalization(fact) else ""}{name1} - {ang_sign if angle_formalization(fact) else ""}{name2} - {name3} = {value if question else value.conversion_to_latex()}{deg_sign if angle_formalization(fact) else ""}'
                else:
                    return f'{ang_sign if angle_formalization(fact) else ""}{name1} - {ang_sign if angle_formalization(fact) else ""}{name2} = {value if question else value.conversion_to_latex()}{deg_sign if angle_formalization(fact) else ""}'
            elif add:
                if len(fact.objects) == 3:
                    name3 = names[2]
                    return f'{ang_sign if angle_formalization(fact) else ""}{name1} + {ang_sign if angle_formalization(fact) else ""}{name2} + {ang_sign if angle_formalization(fact) else ""}{name3} = {value if question else value.conversion_to_latex()}{deg_sign if angle_formalization(fact) else ""}'
                else:
                    return f'{ang_sign if angle_formalization(fact) else ""}{name1} + {ang_sign if angle_formalization(fact) else ""}{name2} = {value if question else value.conversion_to_latex()}{deg_sign if angle_formalization(fact) else ""}'
            else:
                return ""
    except Exception as exc:
        print(exc)
        return ""
