from math import *
from random import *


class MyPoint:
	def __init__(self, x, y, name=None):
		self.x = x
		self.y = y
		self.name = name


class MyLine:
	def __init__(self, a, b, c):
		self.a = a
		self.b = b
		self.c = c


#точка пересечения прямых
def LineIntersectionPoint(L1, L2):
	x = (L1.b*L2.c - L1.c*L2.b)/(L1.a*L2.b - L1.b*L2.a)
	y = (L1.a*L2.c - L1.c*L2.a)/(L1.b*L2.a - L1.a*L2.b)

	return MyPoint(x, y)


#прямая по двум точкам
def TwoPointsLine(P, Q):
	a = P.y - Q.y
	b = Q.x - P.x
	c = -b*P.y - a*P.x

	return MyLine(a, b, c)


#округление
def Equal(x, digits=6):
	return float(f"{x:.{digits}f}")


#перпендикулярная прямая через точку
def PerpendicularLineWithPoint(P, l):
	c = - P.x*l.b + P.y*l.a

	return MyLine(l.b, -l.a, c)


#расстояние между точками
def DistanceBetweenPoints(A, B):
	return sqrt((A.x - B.x)**2 + (A.y - B.y)**2)


#точка, делящая отрезок в заданном отношении k
def DividingPoint(A, B, k):
	return MyPoint((A.x + k*B.x)/(1+k), (A.y + k*B.y)/(1+k))


def CircumscribedCircleCenter(A, B, C):
	BC = TwoPointsLine(B, C)
	AB = TwoPointsLine(A, B)
	M1 = DividingPoint(B, C, 1)
	M3 = DividingPoint(A, B, 1)
	MP1 = PerpendicularLineWithPoint(M1, BC)
	MP3 = PerpendicularLineWithPoint(M3, AB)

	return LineIntersectionPoint(MP1, MP3)


def CirclesIntersectionPoint(r1, r2, O1, O2):
	O = MyPoint(O2.x - O1.x, O2.y - O1.y)
	x = -(r2**2 - r1**2 - O.x**2)/(2*O.x)
	y = sqrt(r1**2 - x**2)

	return MyPoint(x + O1.x, y + O1.y)


def LineWithTiltAngle(P, alpha):
	k = tan(alpha * pi / 180)
	b = P.y - k * P.x

	return MyLine(-k, 1, -b)


def LineAndCircleIntersectionPoints(l, O, r):
	P = LineIntersectionPoint(l, PerpendicularLineWithPoint(O, l))

	try:
		d = sqrt(r**2 - DistanceBetweenPoints(P, O)**2)
		k = -l.a/l.b
		b = -l.c/l.b

		w = 1 + k**2
		p = 2*k*b - 2*k*P.y - 2*P.x
		q = b**2 + P.x**2 + P.y**2 - 2*b*P.y - d**2

		x1 = (-p + sqrt(p**2 - 4*q*w))/(2*w)
		x2 = (-p - sqrt(p**2 - 4*q*w))/(2*w)

		y1 = k*x1 + b
		y2 = k*x2 + b

		return MyPoint(x1, y1), MyPoint(x2, y2)

	except Exception:
		return None


def Shift(A, B, C):
	O = CircumscribedCircleCenter(A, B, C)
	new_A = MyPoint(A.x - O.x, A.y - O.y, A.name)
	new_B = MyPoint(B.x - O.x, B.y - O.y, B.name)
	new_C = MyPoint(C.x - O.x, C.y - O.y, C.name)

	return new_A, new_B, new_C


def CreateTriangleWithThreeSides(a, b, c, angle):
	C = MyPoint(0, 0, angle[1])
	B = MyPoint(a, 0, angle[2])
	A = CirclesIntersectionPoint(b, c, C, B)
	A.name = angle[0]

	return Shift(A, B, C)


def CreateTriangleWithSideAndContraAngle(a, alpha, alpha_name):
	alph = alpha * pi / 180
	C = MyPoint(0, 0, alpha_name[0])
	B = MyPoint(a, 0, alpha_name[2])
	if alpha != 90:
		O = MyPoint(a/2, (1/tan(alph))*(a/2))
	else:
		O = MyPoint(a/2, 0)

	r = DistanceBetweenPoints(O, B)
	x = uniform(-r + a/2, r + a/2)
	y = sqrt(r**2 - (x - a/2)**2) + O.y

	A = MyPoint(x, y, alpha_name[1])
	A, B, C = Shift(A, B, C)

	return A, B, C


def CreateTriangleWithOneSideAndTwoAngles(a, beta, gamma, beta_name, gamma_name):
	C = MyPoint(0, 0, gamma_name[1])
	B = MyPoint(a, 0, beta_name[1])

	l1 = LineWithTiltAngle(C, gamma)
	l2 = LineWithTiltAngle(B, 180 - beta)

	A = LineIntersectionPoint(l1, l2)

	if gamma_name[0] != beta_name[1]:
		A.name = gamma_name[0]
	else:
		A.name = gamma_name[2]

	return Shift(A, B, C)


def CreateTriangleWithTwoSidesAndAngleBetweenThem(a, b, gamma, a_name, gamma_name):
	C = MyPoint(0, 0, gamma_name[1])
	B = MyPoint(a, 0)

	if a_name[0] != gamma_name[1]:
		B.name = a_name[0]
	else:
		B.name = a_name[1]

	l = LineWithTiltAngle(C, gamma)

	k = -l.a
	t = -l.c

	if gamma <= 90:
		x = (-2*t*k + sqrt(4*t**2*k**2 - 4*(k**2 + 1)*(t**2 - b**2))) / (2*(k**2 + 1))
	else:
		x = (-2*t*k - sqrt(4*t**2*k**2 - 4*(k**2 + 1)*(t**2 - b**2))) / (2*(k**2 + 1))
	y = k*x + t

	A = MyPoint(x, y)

	if gamma_name[0] not in a_name:
		A.name = gamma_name[0]
	else:
		A.name = gamma_name[2]

	return Shift(A, B, C)


def CreateTriangleWithTwoSidesAndAngleNotBetweenThem(a, c, gamma, a_name, gamma_name):
	C = MyPoint(0, 0, gamma_name[1])
	B = MyPoint(a, 0)

	if a_name[0] != gamma_name[1]:
		B.name = a_name[0]
	else:
		B.name = a_name[1]

	l = LineWithTiltAngle(C, gamma)
	A1, A2 = LineAndCircleIntersectionPoints(l, B, c)

	if a > c:
		A = choice([A1, A2])
	else:
		if A1.y > A2.y:
			A = A1
		else:
			A = A2

	if gamma_name[0] not in a_name:
		A.name = gamma_name[0]
	else:
		A.name = gamma_name[2]

	return Shift(A, B, C)


def CreateTriangle(sides, angles, angles_names, sides_names):
	if angles.count(None) <= 1:
		test_angle = 180

		for angle in angles:
			if angle:
				test_angle -= angle

		try:
			angles[angles.index(None)] = test_angle
		except Exception:
			pass


		for i in range(3):
			if sides[i]:
				return CreateTriangleWithOneSideAndTwoAngles(sides[i], angles[i-1], angles[(i+1)%3], angles_names[i-1], angles_names[(i+1)%3])
		else:
			random_index = randint(0,2)
			return CreateTriangleWithOneSideAndTwoAngles(uniform(3, 6), angles[random_index-1], angles[(random_index+1)%3], angles_names[random_index-1], angles_names[(random_index+1)%3])

	else:
		for i in range(3):
			if angles[i]:
				if sides[i-1] and sides[(i+1)%3]:
					return CreateTriangleWithTwoSidesAndAngleBetweenThem(sides[i-1], sides[(i+1)%3], angles[i], sides_names[i-1], angles_names[i])
				if sides[i] and sides[i-1]:
					return CreateTriangleWithTwoSidesAndAngleNotBetweenThem(sides[i-1], sides[i], angles[i], sides_names[i-1], angles_names[i])
				if sides[i] and sides[(i+1)%3]:
					return CreateTriangleWithTwoSidesAndAngleNotBetweenThem(sides[(i+1)%3], sides[i], angles[i], sides_names[(i+1)%3], angles_names[i])
				if sides[i]:
					return CreateTriangleWithSideAndContraAngle(sides[i], angles[i], angles_names[i])
				if sides[i-1]:
					return CreateTriangleWithTwoSidesAndAngleBetweenThem(sides[i-1], sides[i-1] * uniform(0.5, 1.5), angles[i], sides_names[i-1], angles_names[i])
				if sides[(i+1)%3]:
					return CreateTriangleWithTwoSidesAndAngleBetweenThem(sides[(i+1)%3], sides[(i+1)%3] * uniform(0.5, 1.5), angles[i], sides_names[(i+1)%3], angles_names[i])
				else:
					return CreateTriangleWithTwoSidesAndAngleBetweenThem(uniform(3, 6), uniform(3, 6), angles[i], sides_names[i-1], angles_names[i])
		else:
			try:
				mean_side = sum(filter(lambda x: x != None, sides)) / (3 - sides.count(None))
			except Exception:
				sides[0] = uniform(3, 6)
				mean_side = sides[0]

			for i in range(3):
				if not sides[i]:
					sides[i] = mean_side * uniform(0.5, 1.5)

			return CreateTriangleWithThreeSides(sides[0], sides[1], sides[2], angles_names[2])