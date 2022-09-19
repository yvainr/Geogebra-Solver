from math import tan, pi
from random import uniform, choice
from ggb_data_processing.objects_types import sqrt
from itertools import combinations


class MyPoint:
	def __init__(self, x, y, name=None):
		self.x = x
		self.y = y
		self.name = name

	def __str__(self):
		return f'{self.name}, {self.x}, {self.y}'


class MyLine:
	def __init__(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c


# точка пересечения прямых
def LineIntersectionPoint(L1, L2):
	x = (L1.b*L2.c - L1.c*L2.b)/(L1.a*L2.b - L1.b*L2.a)
	y = (L1.a*L2.c - L1.c*L2.a)/(L1.b*L2.a - L1.a*L2.b)

	return x, y


# прямая по двум точкам
def TwoPointsLine(P, Q):
	if type(P) != tuple:
		P = (P.x, P.y)
	if type(Q) != tuple:
		Q = (Q.x, Q.y)

	a = P[1] - Q[1]
	b = Q[0] - P[0]
	c = -b * P[1] - a * P[0]

	return MyLine(a, b, c)


def IsLineParallel(L1, L2):
	if abs(L1.a * L2.b - L1.b * L2.a) < 0.00001:
		if L1.a != 0 and L2.a != 0:
			if abs(L1.a * L2.c - L1.c * L2.a) < 0.00001:
				return 2
			else:
				return 0
		else:
			if abs(L1.c - L2.c) < 0.00001:
				return 2
			else:
				return 0
	return 1


def PointOnCircle(O, r):
	if type(O) != tuple:
		O = (O.x, O.y)

	x = O[0] + uniform(-r, r)
	y = sqrt(r**2 - (x - O[0])**2)

	return x, choice((y + O[1], - y + O[1]))


# перпендикулярная прямая через точку
def PerpendicularLineWithPoint(P, l):
	if type(P) == tuple:
		c = - P[0]*l.b + P[1]*l.a
	else:
		c = - P.x*l.b + P.y*l.a

	return MyLine(l.b, -l.a, c)


# расстояние между точками
def DistanceBetweenPoints(A, B):
	if type(A) != tuple:
		A = (A.x, A.y)
	if type(B) != tuple:
		B = (B.x, B.y)

	return sqrt((A[0] - B[0])**2 + (A[1] - B[1])**2)


# точка, делящая отрезок в заданном отношении k
def DividingPoint(A, B, k):
	if type(A) != tuple:
		A = (A.x, A.y)
	if type(B) != tuple:
		B = (B.x, B.y)

	return (A[0] + k * B[0]) / (1 + k), (A[1] + k * B[1]) / (1 + k)


def MediansIntersection(A, B, C):
	M = DividingPoint(A, B, 1)
	N = DividingPoint(B, C, 1)

	CM = TwoPointsLine(C, M)
	AN = TwoPointsLine(A, N)

	return LineIntersectionPoint(CM, AN)


def CircumscribedCircleCenter(A, B, C):
	BC = TwoPointsLine(B, C)
	AB = TwoPointsLine(A, B)

	M1 = DividingPoint(B, C, 1)
	M3 = DividingPoint(A, B, 1)

	MP1 = PerpendicularLineWithPoint(M1, BC)
	MP3 = PerpendicularLineWithPoint(M3, AB)

	return LineIntersectionPoint(MP1, MP3)


def SpecificPointGeneration(point_name, point_specific_name, A, B, C):
	ret = list()

	if point_specific_name == 'O':
		ret.append(f"{A.name}{B.name}{C.name}midperpendicular=PerpendicularLine(Midpoint({A.name}, {C.name}), Line({A.name}, {C.name}))")
		ret.append(f"{B.name}{C.name}{A.name}midperpendicular=PerpendicularLine(Midpoint({B.name}, {A.name}), Line({B.name}, {A.name}))")
		ret.append(f"{C.name}{A.name}{B.name}midperpendicular=PerpendicularLine(Midpoint({C.name}, {B.name}), Line({C.name}, {B.name}))")
		ret.append(f"SetVisibleInView({A.name}{B.name}{C.name}midperpendicular, 1, false)")
		ret.append(f"SetVisibleInView({B.name}{C.name}{A.name}midperpendicular, 1, false)")
		ret.append(f"SetVisibleInView({C.name}{A.name}{B.name}midperpendicular, 1, false)")
		ret.append(f"{point_name}=Intersect({A.name}{B.name}{C.name}midperpendicular, {B.name}{C.name}{A.name}midperpendicular)")
	if point_specific_name == 'I':
		ret.append(f"{A.name}{B.name}{C.name}bisector=AngleBisector({A.name},{B.name},{C.name})")
		ret.append(f"{B.name}{C.name}{A.name}bisector=AngleBisector({B.name},{C.name},{A.name})")
		ret.append(f"{C.name}{A.name}{B.name}bisector=AngleBisector({C.name},{A.name},{B.name})")
		ret.append(f"SetVisibleInView({A.name}{B.name}{C.name}bisector, 1, false)")
		ret.append(f"SetVisibleInView({B.name}{C.name}{A.name}bisector, 1, false)")
		ret.append(f"SetVisibleInView({C.name}{A.name}{B.name}bisector, 1, false)")
		ret.append(f"{point_name}=Intersect({A.name}{B.name}{C.name}bisector, {B.name}{C.name}{A.name}bisector)")
	if point_specific_name == 'H':
		ret.append(f"{A.name}{B.name}{C.name}perpendicular=PerpendicularLine({B.name}, Line({A.name}, {C.name}))")
		ret.append(f"{B.name}{C.name}{A.name}perpendicular=PerpendicularLine({C.name}, Line({B.name}, {A.name}))")
		ret.append(f"{C.name}{A.name}{B.name}perpendicular=PerpendicularLine({A.name}, Line({C.name}, {B.name}))")
		ret.append(f"SetVisibleInView({A.name}{B.name}{C.name}perpendicular, 1, false)")
		ret.append(f"SetVisibleInView({B.name}{C.name}{A.name}perpendicular, 1, false)")
		ret.append(f"SetVisibleInView({C.name}{A.name}{B.name}perpendicular, 1, false)")
		ret.append(f"{point_name}=Intersect({A.name}{B.name}{C.name}perpendicular, {B.name}{C.name}{A.name}perpendicular)")
	if point_specific_name == 'M':
		ret.append(f"{A.name}{B.name}{C.name}median=Line({B.name}, Midpoint({A.name}, {C.name}))")
		ret.append(f"{B.name}{C.name}{A.name}median=Line({C.name}, Midpoint({B.name}, {A.name}))")
		ret.append(f"{C.name}{A.name}{B.name}median=Line({A.name}, Midpoint({C.name}, {B.name}))")
		ret.append(f"SetVisibleInView({A.name}{B.name}{C.name}median, 1, false)")
		ret.append(f"SetVisibleInView({B.name}{C.name}{A.name}median, 1, false)")
		ret.append(f"SetVisibleInView({C.name}{A.name}{B.name}median, 1, false)")
		ret.append(f"{point_name}=Intersect({A.name}{B.name}{C.name}median, {B.name}{C.name}{A.name}median)")

	return ret


def CirclesIntersectionPoint(r1, r2, O1, O2):
	if type(O1) != tuple:
		O1 = (O1.x, O1.y)
	if type(O2) != tuple:
		O2 = (O2.x, O2.y)

	O = (O2[0] - O1[0], O2[1] - O1[1])
	x = -(r2**2 - r1**2 - O[0]**2)/(2*O[0])
	y = sqrt(r1**2 - x**2)

	return x + O1[0], y + O1[1]


def LineWithTiltAngle(P, alpha):
	k = tan((alpha * pi / 180).value)
	if type(P) == tuple:
		b = P[1] - P[0] * k
	else:
		b = P.y - P.x * k

	return MyLine(-k, 1, -b)


def LineAndCircleIntersectionPoints(l, O, r):
	P = LineIntersectionPoint(l, PerpendicularLineWithPoint(O, l))

	d = sqrt(r**2 - DistanceBetweenPoints(P, O)**2)
	k = -l.a/l.b
	b = -l.c/l.b

	w = 1 + k**2
	p = 2*k*b - 2*k*P[1] - 2*P[0]
	q = b**2 + P[0]**2 + P[1]**2 - 2*b*P[1] - d**2

	x1 = (-p + sqrt(p**2 - 4*q*w))/(2*w)
	x2 = (-p - sqrt(p**2 - 4*q*w))/(2*w)

	y1 = k*x1 + b
	y2 = k*x2 + b

	return (x1, y1), (x2, y2)


def PointSymmetryAboutLine(P, l1):
	l2 = PerpendicularLineWithPoint(P, l1)
	x, y = LineIntersectionPoint(l1, l2)

	return 2 * x - P.x, 2 * y - P.y


def CheckSegmentsIntersection(side1, side2):
	A1, B1 = side1
	A2, B2 = side2

	l1 = TwoPointsLine(A1, B1)
	l2 = TwoPointsLine(A2, B2)

	try:
		x, y = LineIntersectionPoint(l1, l2)
		return min(A1.x, B1.x) <= x <= max(A1.x, B1.x) and min(A2.x, B2.x) <= x <= max(A2.x, B2.x) and min(A1.y, B1.y) <= y <= max(A1.y, B1.y) and min(A2.y, B2.y) <= y <= max(A2.y, B2.y)

	except Exception:
		return IsLineParallel(l1, l2) == 2 and (min(A1.x, B1.x) <= max(A2.x, B2.x) or min(A2.x, B2.x) <= max(A1.x, B1.x))


def CheckTrianglesIntersection(tr1, tr2):
	M1 = MediansIntersection(*tr1)
	M2 = MediansIntersection(*tr2)

	for point in tr1:
		if DistanceBetweenPoints(M2, point) < (max(DistanceBetweenPoints(M2, tr2[0]), DistanceBetweenPoints(M2, tr2[1]), DistanceBetweenPoints(M2, tr2[2])) + 1):
			return True

	for point in tr2:
		if DistanceBetweenPoints(M1, point) < (max(DistanceBetweenPoints(M1, tr1[0]), DistanceBetweenPoints(M1, tr1[1]), DistanceBetweenPoints(M1, tr1[2])) + 1):
			return True

	for side1 in combinations(tr1, 2):
		for side2 in combinations(tr2, 2):
			if CheckSegmentsIntersection(side1, side2):
				return True

	return False
