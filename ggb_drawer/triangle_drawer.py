from ggb_data_processing import task_parser as tp
from math import tan, pi, cos, sin, acos
from random import choice, uniform, randint
from itertools import combinations
from ggb_data_processing.objects_types import Size, sqrt
from ggb_drawer.useful_geometry_functions import LineIntersectionPoint, TwoPointsLine, IsLineParallel,\
	PerpendicularLineWithPoint, DistanceBetweenPoints, DividingPoint, MediansIntersection, CircumscribedCircleCenter, \
	CirclesIntersectionPoint, LineWithTiltAngle, LineAndCircleIntersectionPoints, PointSymmetryAboutLine


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


def RandomRotation(A, B, C):
	x, y = CircumscribedCircleCenter(A, B, C)

	A.x -= x
	A.y -= y
	B.x -= x
	B.y -= y
	C.x -= x
	C.y -= y

	phi = uniform(-pi, pi)

	A.x, A.y = A.x * cos(phi) - A.y * sin(phi), A.y * cos(phi) + A.x * sin(phi)
	B.x, B.y = B.x * cos(phi) - B.y * sin(phi), B.y * cos(phi) + B.x * sin(phi)
	C.x, C.y = C.x * cos(phi) - C.y * sin(phi), C.y * cos(phi) + C.x * sin(phi)

	A.x += x
	A.y += y
	B.x += x
	B.y += y
	C.x += x
	C.y += y

	return A, B, C


def Shift(A, B, C):
	A, B, C = RandomRotation(A, B, C)

	phi = uniform(-pi, pi)
	vec = (cos(phi) * 2, sin(phi) * 2)

	if set(tp.get_points_names_from_list(tp.solver_data.polygons[0].points)) != {A.name, B.name, C.name}:
		while True:
			stop = True

			for polygon in tp.solver_data.polygons:
				if set(tp.get_points_names_from_list(polygon.points)) != {A.name, B.name, C.name}:

					if CheckTrianglesIntersection(polygon.points, (A, B, C)):
						A.x += vec[0]
						A.y += vec[1]
						B.x += vec[0]
						B.y += vec[1]
						C.x += vec[0]
						C.y += vec[1]

						stop = False
						break

				else:
					break

			if stop:
				break

	return SaveTriangleData(A, B, C)


def SaveTriangleData(A, B, C):
	AB = tp.find_segment_with_points(A.name, B.name)
	BC = tp.find_segment_with_points(B.name, C.name)
	CA = tp.find_segment_with_points(C.name, A.name)

	if not AB.size:
		AB.size = DistanceBetweenPoints(A, B)
	for rel in AB.relations:
		if not rel.size:
			rel.size = AB.size / AB.relations[rel]
	if not BC.size:
		BC.size = DistanceBetweenPoints(B, C)
	for rel in BC.relations:
		if not rel.size:
			rel.size = BC.size / BC.relations[rel]
	if not CA.size:
		CA.size = DistanceBetweenPoints(C, A)
	for rel in CA.relations:
		if not rel.size:
			rel.size = CA.size / CA.relations[rel]

	ACB = tp.find_angle_with_points(A.name, C.name, B.name)
	BAC = tp.find_angle_with_points(B.name, A.name, C.name)
	CBA = tp.find_angle_with_points(C.name, B.name, A.name)

	if not CBA.size:
		CBA.size = Size(acos(((BC.size ** 2 + AB.size ** 2 - CA.size ** 2) / (2 * BC.size * AB.size)).value) * 180 / pi)
	for rel in CBA.relations:
		if not rel.size:
			rel.size = CBA.size / CBA.relations[rel]
	if not ACB.size:
		ACB.size = Size(acos(((BC.size ** 2 + CA.size ** 2 - AB.size ** 2) / (2 * BC.size * CA.size)).value) * 180 / pi)
	for rel in ACB.relations:
		if not rel.size:
			rel.size = ACB.size / ACB.relations[rel]
	if not BAC.size:
		BAC.size = Size(acos(((AB.size ** 2 + CA.size ** 2 - BC.size ** 2) / (2 * AB.size * CA.size)).value) * 180 / pi)
	for rel in BAC.relations:
		if not rel.size:
			rel.size = BAC.size / BAC.relations[rel]

	return A, B, C


def CheckQuadrangleConvex(A, B, C, D):
	t1 = (D.x - A.x)*(B.y - A.y) - (D.y - A.y)*(B.x - A.x)
	t2 = (D.x - B.x)*(C.y - B.y) - (D.y - B.y)*(C.x - B.x)
	t3 = (D.x - C.x)*(A.y - C.y) - (D.y - C.y)*(A.x - C.x)
	t4 = (A.x - C.x)*(B.y - C.y) - (A.y - C.y)*(B.x - C.x)

	return t1 * t2 * t3 * t4 > 0


def CreateTriangleWithThreeSides(a, b, c, angle):
	C = tp.find_point_with_name(angle[0])
	C.x, C.y = Size(0), Size(0)
	B = tp.find_point_with_name(angle[1])
	B.x, B.y = a, Size(0)
	A = tp.find_point_with_name(angle[2])
	A.x, A.y = CirclesIntersectionPoint(b, c, C, B)

	return Shift(A, B, C)


def CreateTriangleWithSideAndContraAngle(a, alpha, alpha_name):
	alph = alpha * pi / 180
	C = tp.find_point_with_name(alpha_name[2])
	C.x, C.y = Size(0), Size(0)
	B = tp.find_point_with_name(alpha_name[0])
	B.x, B.y = a, Size(0)
	if alpha != 90:
		O = (a/2, (1/tan(alph))*(a/2))
	else:
		O = (a/2, 0)

	r = DistanceBetweenPoints(O, B)
	x = uniform(-r + a/2, r + a/2)
	y = sqrt(r**2 - (x - a/2)**2) + O[1]

	A = tp.find_point_with_name(alpha_name[1])
	A.x, A.y = x, y

	return Shift(A, B, C)


def CreateTriangleWithOneSideAndTwoAngles(a, beta, gamma, beta_name, gamma_name):
	B = tp.find_point_with_name(beta_name[1])
	B.x, B.y = Size(0), Size(0)
	C = tp.find_point_with_name(gamma_name[1])
	C.x, C.y = a, Size(0)

	l1 = LineWithTiltAngle(C, Size(180) - gamma)
	l2 = LineWithTiltAngle(B, beta)

	if gamma_name[0] != beta_name[1]:
		A = tp.find_point_with_name(gamma_name[0])

	else:
		A = tp.find_point_with_name(gamma_name[2])

	A.x, A.y = LineIntersectionPoint(l1, l2)

	return Shift(A, B, C)


def CreateTriangleWithTwoSidesAndAngleBetweenThem(a, b, gamma, a_name, gamma_name):
	if a_name[0] != gamma_name[1]:
		C = tp.find_point_with_name(a_name[0])
	else:
		C = tp.find_point_with_name(a_name[1])

	C.x, C.y = Size(0), Size(0)
	B = tp.find_point_with_name(gamma_name[1])
	B.x, B.y = a, Size(0)

	l = LineWithTiltAngle(C, gamma)
	k = -l.a
	t = -l.c

	if gamma <= 90:
		x = (-2*t*k + sqrt(4*t**2*k**2 - 4*(k**2 + 1)*(t**2 - b**2))) / (2*(k**2 + 1))
	else:
		x = (-2*t*k - sqrt(4*t**2*k**2 - 4*(k**2 + 1)*(t**2 - b**2))) / (2*(k**2 + 1))
	y = k*x + t

	if gamma_name[0] not in a_name:
		A = tp.find_point_with_name(gamma_name[0])
	else:
		A = tp.find_point_with_name(gamma_name[2])

	A.x, A.y = x, y
	A.x, A.y = PointSymmetryAboutLine(A, PerpendicularLineWithPoint(DividingPoint(B, C, 1), TwoPointsLine(B, C)))

	return Shift(A, B, C)


def CreateTriangleWithTwoSidesAndAngleNotBetweenThem(a, c, gamma, a_name, gamma_name):
	if a_name[0] != gamma_name[1]:
		C = tp.find_point_with_name(gamma_name[1])
		C.x, C.y = Size(0), Size(0)
		B = tp.find_point_with_name(a_name[0])
		B.x, B.y = a, Size(0)
		make_simmetry = False
	else:
		C = tp.find_point_with_name(a_name[1])
		C.x, C.y = Size(0), Size(0)
		B = tp.find_point_with_name(gamma_name[1])
		B.x, B.y = a, Size(0)
		make_simmetry = True

	if gamma_name[0] not in a_name:
		A = tp.find_point_with_name(gamma_name[0])
	else:
		A = tp.find_point_with_name(gamma_name[2])

	A1, A2 = LineAndCircleIntersectionPoints(LineWithTiltAngle(C, gamma), B, c)

	if a > c:
		A.x, A.y = choice([A1, A2])
	else:
		if A1[1] > A2[1]:
			A.x, A.y = A1
		else:
			A.x, A.y = A2

	if make_simmetry:
		A.x, A.y = PointSymmetryAboutLine(A, PerpendicularLineWithPoint(DividingPoint(B, C, 1), TwoPointsLine(B, C)))

	return Shift(A, B, C)


def CreateTriangle(sides, angles, sides_names, angles_names):
	if [angles[0].size, angles[1].size, angles[2].size].count(None) <= 1:
		test_angle = Size(180)

		for angle in angles:
			if angle.size:
				test_angle -= angle.size

		for angle in angles:
			if not angle.size:
				angle.size = test_angle

		for i in range(3):
			if sides[i].size:
				return CreateTriangleWithOneSideAndTwoAngles(sides[i].size, angles[i - 1].size, angles[i - 2].size, angles_names[i - 1], angles_names[i - 2])
		else:
			random_index = randint(0, 2)
			return CreateTriangleWithOneSideAndTwoAngles(uniform(3, 6), angles[random_index - 1].size, angles[random_index - 2].size, angles_names[random_index - 1], angles_names[random_index - 2])

	else:
		for i in range(3):
			if angles[i].size:
				if sides[i - 1].size and sides[i - 2].size:
					return CreateTriangleWithTwoSidesAndAngleBetweenThem(sides[i - 1].size, sides[i - 2].size, angles[i].size, sides_names[i - 1], angles_names[i])
				if sides[i].size and sides[i - 1].size:
					return CreateTriangleWithTwoSidesAndAngleNotBetweenThem(sides[i - 1].size, sides[i].size, angles[i].size, sides_names[i - 1], angles_names[i])
				if sides[i].size and sides[i - 2].size:
					return CreateTriangleWithTwoSidesAndAngleNotBetweenThem(sides[i - 2].size, sides[i].size, angles[i].size, sides_names[i - 2], angles_names[i])
				if sides[i].size:
					return CreateTriangleWithSideAndContraAngle(sides[i].size, angles[i].size, angles_names[i])
				if sides[i - 1].size:
					return CreateTriangleWithTwoSidesAndAngleBetweenThem(sides[i - 1].size, sides[i - 1].size * uniform(0.5, 1.5), angles[i].size, sides_names[i - 1], angles_names[i])
				if sides[i - 2].size:
					return CreateTriangleWithTwoSidesAndAngleBetweenThem(sides[i - 2].size, sides[i - 2].size * uniform(0.5, 1.5), angles[i].size, sides_names[i - 2], angles_names[i])
				else:
					sides[i - 1].size = Size(uniform(3, 6))

					for rel in sides[i - 1].relations:
						if rel == sides[i - 2]:
							sides[i - 2].size = sides[i - 1].size / sides[i - 1].relations[rel]
					else:
						sides[i - 2].size = Size(uniform(3, 6))

					return CreateTriangleWithTwoSidesAndAngleBetweenThem(sides[i - 1].size, sides[i - 2].size, angles[i].size, sides_names[i - 1], angles_names[i])
		else:
			if [sides[0].size, sides[1].size, sides[2].size].count(None) == 3:
				ind = 0

				for i in range(3):
					if sides[i - 1] in sides[i].relations and sides[i - 2] in sides[i].relations:
						ind = i
						break
					elif sides[i - 1] in sides[i].relations or sides[i - 2] in sides[i].relations:
						ind = i

				sides[ind].size = Size(uniform(3, 6))

				try:
					sides[ind - 1].size = sides[ind].size / sides[ind].relations[sides[ind - 1]]
				except KeyError:
					pass

				try:
					sides[ind - 2].size = sides[ind].size / sides[ind].relations[sides[ind - 2]]
				except KeyError:
					pass

			if [sides[0].size, sides[1].size, sides[2].size].count(None) == 2:

				for side in sides:
					if side.size:
						i = sides.index(side)

				if sides[i - 2] in sides[i - 1].relations:
					sides[i - 1].size = uniform(sides[i].size * 1.25, sides[i].size * 3) / (1 + 1 / sides[i - 1].relations[sides[i - 2]])
					sides[i - 2].size = sides[i - 1].size / sides[i - 1].relations[sides[i - 2]]

					while min(sides[i - 1].size, sides[i - 2].size) + sides[i].size <= max(sides[i - 1].size, sides[i - 2].size):
						sides[i - 1].size *= 0.8
						sides[i - 2].size *= 0.8

				else:
					sides[i - 1].size = sides[i].size * uniform(0.5, 1.5)

			if [sides[0].size, sides[1].size, sides[2].size].count(None) == 1:

				i = [sides[0].size, sides[1].size, sides[2].size].index(None)
				sides[i].size = uniform(abs(sides[i - 1].size - sides[i - 2].size), sides[i - 1].size + sides[i - 2].size)

			return CreateTriangleWithThreeSides(sides[0].size, sides[1].size, sides[2].size, angles_names[1])
