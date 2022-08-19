import task_parser as tp
from math import tan, pi, cos, sin, acos
from random import choice, uniform, randint
from itertools import combinations
from objects_types import Size, sqrt


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


# #округление
# def Equal(x, digits=6):
# 	return float(f"{float(x.value):.{digits}f}")


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
	O = MyPoint(O2.x - O1.x, O2.y - O1.y)
	x = -(r2**2 - r1**2 - O.x**2)/(2*O.x)
	y = sqrt(r1**2 - x**2)
	
	return MyPoint(x + O1.x, y + O1.y)


def LineWithTiltAngle(P, alpha):
	k = tan((alpha * pi / 180).value)
	b = P.y - P.x * k
	
	return MyLine(-k, 1, -b)


def LineAndCircleIntersectionPoints(l, O, r):
	P = LineIntersectionPoint(l, PerpendicularLineWithPoint(O, l))

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


def CheckSegmentsIntersection(side1, side2):
	A1, B1 = side1
	A2, B2 = side2

	l1 = TwoPointsLine(A1, B1)
	l2 = TwoPointsLine(A2, B2)

	try:
		P = LineIntersectionPoint(l1, l2)
		return min(A1.x, B1.x) <= P.x <= max(A1.x, B1.x) and min(A2.x, B2.x) <= P.x <= max(A2.x, B2.x) and min(A1.y, B1.y) <= P.y <= max(A1.y, B1.y) and min(A2.y, B2.y) <= P.y <= max(A2.y, B2.y)

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


def RandomRotation(A, B, C):
	O = CircumscribedCircleCenter(A, B, C)

	A.x -= O.x
	A.y -= O.y
	B.x -= O.x
	B.y -= O.y
	C.x -= O.x
	C.y -= O.y

	phi = uniform(-pi, pi)

	A.x, A.y = A.x * cos(phi) - A.y * sin(phi), A.y * cos(phi) + A.x * sin(phi)
	B.x, B.y = B.x * cos(phi) - B.y * sin(phi), B.y * cos(phi) + B.x * sin(phi)
	C.x, C.y = C.x * cos(phi) - C.y * sin(phi), C.y * cos(phi) + C.x * sin(phi)

	A.x += O.x
	A.y += O.y
	B.x += O.x
	B.y += O.y
	C.x += O.x
	C.y += O.y

	return A, B, C
		
	
def Shift(new_A, new_B, new_C):

	new_A, new_B, new_C = RandomRotation(new_A, new_B, new_C)

	phi = uniform(-pi, pi)
	vec = (cos(phi) * 2, sin(phi) * 2)

	if set(tp.get_points_names_from_list(tp.solver_data.polygons[0].points)) != {new_A.name, new_B.name, new_C.name}:
		while True:
			stop = True

			for polygon in tp.solver_data.polygons:
				if set(tp.get_points_names_from_list(polygon.points)) != {new_A.name, new_B.name, new_C.name}:

					if CheckTrianglesIntersection(polygon.points, (new_A, new_B, new_C)):
						new_A.x += vec[0]
						new_A.y += vec[1]
						new_B.x += vec[0]
						new_B.y += vec[1]
						new_C.x += vec[0]
						new_C.y += vec[1]

						stop = False
						break

				else:
					break

			if stop:
				break

	return SaveTriangleData(new_A, new_B, new_C)


def PointSymmetryAboutLine(P, l1):
	l2 = PerpendicularLineWithPoint(P, l1)
	Q = LineIntersectionPoint(l1, l2)
	
	return MyPoint(2 * Q.x - P.x, 2 * Q.y - P.y, P.name)


def SaveTriangleData(A, B, C):
	new_A = tp.find_point_with_name(A.name)
	new_B = tp.find_point_with_name(B.name)
	new_C = tp.find_point_with_name(C.name)

	if not new_A.x:
		new_A.x = A.x
		new_A.y = A.y
	if not new_B.x:
		new_B.x = B.x
		new_B.y = B.y
	if not new_C.x:
		new_C.x = C.x
		new_C.y = C.y

	AB = tp.find_segment_with_points(A.name, B.name)
	BC = tp.find_segment_with_points(C.name, B.name)
	AC = tp.find_segment_with_points(A.name, C.name)

	if not AB.size:
		AB.size = DistanceBetweenPoints(A, B)
	if not BC.size:
		BC.size = DistanceBetweenPoints(C, B)
	if not AC.size:
		AC.size = DistanceBetweenPoints(A, C)

	CBA = tp.find_angle_with_points(new_C.name, new_B.name, new_A.name)
	ACB = tp.find_angle_with_points(new_A.name, new_C.name, new_B.name)
	BAC = tp.find_angle_with_points(new_B.name, new_A.name, new_C.name)

	c = AB.size
	a = BC.size
	b = AC.size

	if not CBA.size:
		CBA.size = Size(acos(((a ** 2 + c ** 2 - b ** 2) / (2 * a * c)).value) * 180 / pi)
	if not ACB.size:
		ACB.size = Size(acos(((a ** 2 + b ** 2 - c ** 2) / (2 * a * b)).value) * 180 / pi)
	if not BAC.size:
		BAC.size = Size(acos(((c ** 2 + b ** 2 - a ** 2) / (2 * c * b)).value) * 180 / pi)

	return new_A, new_B, new_C


def CheckQuadrangleConvex(A, B, C, D):
	t1 = (D.x - A.x)*(B.y - A.y) - (D.y - A.y)*(B.x - A.x)
	t2 = (D.x - B.x)*(C.y - B.y) - (D.y - B.y)*(C.x - B.x)
	t3 = (D.x - C.x)*(A.y - C.y) - (D.y - C.y)*(A.x - C.x)
	t4 = (A.x - C.x)*(B.y - C.y) - (A.y - C.y)*(B.x - C.x)

	return t1 * t2 * t3 * t4 > 0


def CreateTriangleWithThreeSides(a, b, c, angle):
	C = MyPoint(Size('0'), Size('0'), angle[0])
	B = MyPoint(a, Size('0'), angle[1])
	A = CirclesIntersectionPoint(b, c, C, B)
	A.name = angle[2]

	return Shift(A, B, C)


def CreateTriangleWithSideAndContraAngle(a, alpha, alpha_name):
	alph = alpha * pi / 180
	C = MyPoint(0, 0, alpha_name[2])
	B = MyPoint(a, 0, alpha_name[0])
	if alpha != 90:
		O = MyPoint(a/2, (1/tan(alph))*(a/2))
	else:
		O = MyPoint(a/2, 0)
	
	r = DistanceBetweenPoints(O, B)
	x = uniform(-r + a/2, r + a/2)
	y = sqrt(r**2 - (x - a/2)**2) + O.y
	
	A = MyPoint(x, y, alpha_name[1])
	
	return Shift(A, B, C)


def CreateTriangleWithOneSideAndTwoAngles(a, beta, gamma, beta_name, gamma_name):
	B = MyPoint(Size('0'), Size('0'), beta_name[1])
	C = MyPoint(a, Size('0'), gamma_name[1])
	
	l1 = LineWithTiltAngle(C, Size('180') - gamma)
	l2 = LineWithTiltAngle(B, beta)
	
	A = LineIntersectionPoint(l1, l2)
	
	if gamma_name[0] != beta_name[1]:
		A.name = gamma_name[0]
	else:
		A.name = gamma_name[2]

	return Shift(A, B, C)


def CreateTriangleWithTwoSidesAndAngleBetweenThem(a, b, gamma, a_name, gamma_name):
	C = MyPoint(Size('0'), Size('0'))
	B = MyPoint(a, Size('0'), gamma_name[1])
	
	if a_name[0] != gamma_name[1]:
		C.name = a_name[0]
	else:
		C.name = a_name[1]
	
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

	A = PointSymmetryAboutLine(A, PerpendicularLineWithPoint(DividingPoint(B, C, 1), TwoPointsLine(B, C)))
	
	return Shift(A, B, C)


def CreateTriangleWithTwoSidesAndAngleNotBetweenThem(a, c, gamma, a_name, gamma_name):
	C = MyPoint(Size('0'), Size('0'))
	B = MyPoint(a, Size('0'))
		
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

	if a_name[0] != gamma_name[1]:
		C.name = gamma_name[1]
		B.name = a_name[0]
	else:
		C.name = a_name[1]
		B.name = gamma_name[1]
		A = PointSymmetryAboutLine(A, PerpendicularLineWithPoint(DividingPoint(B, C, 1), TwoPointsLine(B, C)))

	return Shift(A, B, C)
	
	
def CreateTriangle(sides, angles, angles_names, sides_names):
	if angles.count(None) <= 1:
		test_angle = Size('180')
		
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
			if sides.count(None) == 3:
				sides[0] = uniform(3, 5)
				
			if sides.count(None) == 2:
				for side in sides:
					if side:
						i = sides.index(side)
				sides[i-1] = sides[i] * uniform(0.5, 1.5)
				
			if sides.count(None) == 1:
				i = sides.index(None)
				sides[i] = uniform(abs(sides[i-1] - sides[(i+1)%3]), sides[i-1] + sides[(i+1)%3])
			
			return CreateTriangleWithThreeSides(sides[0], sides[1], sides[2], angles_names[1])
