import Solver_alpha
import task_parser as taskp
from re import *


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
        if isinstance(item, taskp.Angle):
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

        if angle_formalization(fact):
            if equality:
                return "{S}{N1} = {S}{N2}".format(N1=names[0], N2=names[1], S=u"\u2220")
            elif relation:
                return "{S}{N1}/{S}{N2} = {V}".format(N1=names[0], N2=names[1], V=value, S=u"\u2220")
            elif size:
                return "{S}{N1} = {V}{D}".format(N1=names[0], V=value, D=u"\N{DEGREE SIGN}", S=u"\u2220")
            elif diff:
                if len(fact.objects) == 3:
                    return "{S}{N1} - {S}{N2} - {N3} = {V}{D}".format(N1=names[0], N2=names[1],  N3=names[2], V=value, D=u"\N{DEGREE SIGN}", S=u"\u2220")
                else:
                    return "{S}{N1} - {S}{N2} = {V}{D}".format(N1=names[0], N2=names[1], V=value, D=u"\N{DEGREE SIGN}", S=u"\u2220")
            elif add:
                if len(fact.objects) == 3:
                    return "{S}{N1} + {S}{N2} + {S}{N3} = {V}{D}".format(N1=names[0], N2=names[1], N3=names[2], V=value, D=u"\N{DEGREE SIGN}", S=u"\u2220")
                else:
                    return "{S}{N1} + {S}{N2} = {V}{D}".format(N1=names[0], N2=names[1], V=value, D=u"\N{DEGREE SIGN}", S=u"\u2220")
            else:
                return ""
        else:
            if equality:
                return "{N1} = {N2}".format(N1=names[0], N2=names[1])
            elif relation:
                return "{N1}/{N2} = {V}".format(N1=names[0], N2=names[1], V=value)
            elif size:
                return "{N1} = {V}".format(N1=names[0], V=value)
            elif diff:
                if len(fact.objects) == 3:
                    return "{N1} - {N2} - {N3} = {V}".format(N1=names[0], N2=names[1], N3=names[2], V=value)
                else:
                    return "{N1} - {N2} = {V}".format(N1=names[0], N2=names[1], V=value)
            elif add:
                if len(fact.objects) == 3:
                    return "{N1} + {N2} + {N3} = {V}".format(N1=names[0], N2=names[1], N3=names[2], V=value)
                else:
                    return "{N1} + {N2} = {V}".format(N1=names[0], N2=names[1], V=value)
            else:
                return ""
    except:
        return ""



