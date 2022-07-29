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
