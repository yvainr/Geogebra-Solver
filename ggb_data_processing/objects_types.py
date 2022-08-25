import math
from fractions import Fraction


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


class Size:
    def __init__(self, value, outward_type='usual'):
        # if value.__class__.__name__ == 'str':
        #     self.value = Fraction(value)
        # elif value.__class__.__name__ == 'Fraction':
        #     self.value = Fraction(value)
        # else:
        #     print(f'Ошибка работы со значением, value={value}, type={value.__class__.__name__}')

        if outward_type == 'usual':
            self.value = Fraction(value)
            if len(str(self.value)) < 5 and '/' in str(self.value):
                self.outward = str(self.value)
            else:
                self.outward = str(f"{float(self.value):.{2}f}").replace('.00', '')
        elif outward_type == 'sqrt':
            self.value = Fraction(math.sqrt(value))
            if len(str(self.value)) < 5 and '/' in str(self.value):
                self.outward = str(self.value)
            else:
                if len(str(float(self.value)).split('.')[1]) < 3:
                    self.outward = str(f"{float(self.value):.{2}f}").replace('.00', '')
                else:
                    if len(str(Fraction(value))) < 5 and '/' in str(Fraction(value)):
                        self.outward = f'√{str(Fraction(value))}'
                    else:
                        self.outward = f'√{str(f"{float(value):.{2}f}").replace(".00", "")}'

    def __neg__(self):
        return Size(-self.value)

    def __add__(self, other):
        return Size(get_values(self) + get_values(other))

    def __radd__(self, other):
        return Size(get_values(self) + get_values(other))

    def __sub__(self, other):
        return Size(get_values(self) - get_values(other))

    def __rsub__(self, other):
        return Size(get_values(other) - get_values(self))

    def __truediv__(self, other):
        return Size(get_values(self) / get_values(other))

    def __rtruediv__(self, other):
        return Size(get_values(other) / get_values(self))

    def __mul__(self, other):
        return Size(get_values(self) * get_values(other))

    def __rmul__(self, other):
        return Size(get_values(self) * get_values(other))

    def __pow__(self, other):
        return Size(get_values(self) ** get_values(other))

    def __rpow__(self, other):
        return Size(get_values(other) ** get_values(self))

    def __lt__(self, other):
        return get_values(self) < get_values(other)

    def __le__(self, other):
        return get_values(self) <= get_values(other)

    def __eq__(self, other):
        return get_values(self) == get_values(other)

    def __ne__(self, other):
        return get_values(self) != get_values(other)

    def __ge__(self, other):
        return get_values(self) >= get_values(other)

    def __gt__(self, other):
        return get_values(self) > get_values(other)

    def __abs__(self):
        return Size(abs(self.value))

    def __float__(self):
        return float(self.value)

    def __round__(self, n=None):
        return round(self.value, n)

    def conversion_to_latex(self):
        if '√' in self.outward:
            proccesed_outward = self.outward[1:]
            if '/' in proccesed_outward:
                numerator, denominator = proccesed_outward.split('/')
                proccesed_outward = '\( \\frac{' + numerator + '}{' + denominator + '} \)'
            proccesed_outward = '\( \sqrt{' + proccesed_outward + '} \)'
        else:
            proccesed_outward = self.outward
            if '/' in proccesed_outward:
                numerator, denominator = proccesed_outward.split('/')
                proccesed_outward = '\( \\frac{' + numerator + '}{' + denominator + '} \)'
                
        return proccesed_outward

    def __str__(self):
        return f'{self.outward}'


def get_values(obj):
    if obj.__class__.__name__ == 'Size':
        return obj.value
    return obj


def sqrt(obj):
    if obj.__class__.__name__ == 'Size':
        return Size(obj.value, 'sqrt')
    return math.sqrt(obj)


# print(Size('1/4').sqrt())
