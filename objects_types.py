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

    for point in objects.points:
        ret.points.append(point)
    for line in objects.lines:
        ret.lines.append(line)
    for ray in objects.rays:
        ret.rays.append(ray)
    for angle in objects.angles:
        ret.angles.append(angle)
    for segment in objects.segments:
        ret.segments.append(segment)
    for polygon in objects.polygons:
        ret.polygons.append(polygon)
    for fact in objects.facts:
        ret.facts.append(fact)
    for question in objects.questions:
        ret.questions.append(question)

    return ret
