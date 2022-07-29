from copy import deepcopy


class Objects:
    def __init__(self):
        self.points = list()
        self.lines = list()
        self.rays = list()
        self.angles = list()
        self.segments = list()
        self.polygons = list()
        self.facts = list()
        self.questions = list()

    def __str__(self):
        return f'{self.points}\n{self.lines}\n{self.rays}\n{self.angles}\n{self.segments}\n{self.polygons}\n{self.facts}\n{self.questions}'


def create_objects_copy(objects):
    ret = Objects()

    ret.points = deepcopy(objects.points)
    ret.lines = deepcopy(objects.lines)
    ret.rays = deepcopy(objects.rays)
    ret.angles = deepcopy(objects.angles)
    ret.segments = deepcopy(objects.segments)
    ret.polygons = deepcopy(objects.polygons)
    ret.facts = deepcopy(objects.facts)
    ret.questions = deepcopy(objects.questions)

    return ret
