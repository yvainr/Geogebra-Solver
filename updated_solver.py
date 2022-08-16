import task_parser as tp
from itertools import combinations, permutations
from objects_types import Size, sqrt
# from math import sqrt


def count_sizes_of_angles_and_segments(objects, facts_generation, actual_question):
    none_count = 0

    for obj in objects:
        if not obj.size:
            none_count += 1

    if none_count == len(objects):
        return None

    for n in range(none_count):

        for i in range(len(objects)):
            obj_1 = objects[i]
            if not obj_1.size:

                for j in range(len(objects)):
                    obj_2 = objects[j]
                    if obj_2.size:

                        try:
                            obj_1.size = obj_2.size / obj_2.relations[obj_1]
                            new_fact = tp.Fact(
                                len(tp.solver_data.facts),
                                facts_generation,
                                'size',
                                [obj_1],
                                obj_1.size
                            )
                            tp.solver_data.facts.append(new_fact)
                            new_fact.root_facts.add(find_fact_id_with_objects([obj_2], 'size'))
                            new_fact.root_facts.add(create_fact_about_objects_relations([obj_2, obj_1], facts_generation))

                            if new_fact.objects == actual_question.objects and new_fact.fact_type == actual_question.fact_type:
                                return True

                        except KeyError:
                            try:
                                obj_1.size = obj_2.size - obj_2.difference[obj_1]
                                new_fact = tp.Fact(
                                    len(tp.solver_data.facts),
                                    facts_generation,
                                    'size',
                                    [obj_1],
                                    obj_1.size
                                )
                                tp.solver_data.facts.append(new_fact)
                                new_fact.root_facts.add(find_fact_id_with_objects([obj_2], 'size'))
                                new_fact.root_facts.add(find_fact_id_with_objects([obj_2, obj_1], 'difference'))

                                if new_fact.objects == actual_question.objects and new_fact.fact_type == actual_question.fact_type:
                                    return True

                            except KeyError:
                                try:
                                    obj_1.size = obj_2.addition[obj_1] - obj_2.size
                                    new_fact = tp.Fact(
                                        len(tp.solver_data.facts),
                                        facts_generation,
                                        'size',
                                        [obj_1],
                                        obj_1.size
                                    )
                                    tp.solver_data.facts.append(new_fact)
                                    new_fact.root_facts.add(find_fact_id_with_objects([obj_2], 'size'))
                                    new_fact.root_facts.add(find_fact_id_with_objects({obj_2, obj_1}, 'addition'))

                                    if new_fact.objects == actual_question.objects and new_fact.fact_type == actual_question.fact_type:
                                        return True

                                except KeyError:
                                    pass


def count_sides_and_angles_of_similar_polygons(facts_generation, actual_question):
    for i in range(len(tp.solver_data.polygons) - 1):
        for j in range(i + 1, len(tp.solver_data.polygons)):
            polygon_1 = tp.solver_data.polygons[i]
            polygon_2 = tp.solver_data.polygons[j]

            try:
                rel = polygon_1.relations[polygon_2]

            except KeyError:
                try:
                    rel = 1 / polygon_2.relations[polygon_1]

                except KeyError:
                    rel = None

            if rel:
                for k in range(len(polygon_1.points)):
                    seg_1 = tp.find_segment_with_points(polygon_1.points[k - 1].name, polygon_1.points[k].name,
                                                        tp.solver_data)
                    seg_2 = tp.find_segment_with_points(polygon_2.points[k - 1].name, polygon_2.points[k].name,
                                                        tp.solver_data)

                    try:
                        seg_1.relations[seg_2]

                    except KeyError:
                        seg_1.relations[seg_2] = rel

                        new_fact = tp.Fact(
                            len(tp.solver_data.facts),
                            facts_generation,
                            'relation',
                            [seg_1, seg_2],
                            rel
                        )
                        tp.solver_data.facts.append(new_fact)
                        new_fact.root_facts.add(find_fact_id_with_objects([polygon_1, polygon_2], 'relation'))
                        new_fact.description = 'из подобия многоугольников'

                        if new_fact.objects == actual_question.objects and new_fact.fact_type == actual_question.fact_type:
                            return True

                    try:
                        seg_2.relations[seg_1]

                    except KeyError:
                        seg_2.relations[seg_1] = 1 / rel

                        new_fact = tp.Fact(
                            len(tp.solver_data.facts),
                            facts_generation,
                            'relation',
                            [seg_2, seg_1],
                            1 / rel
                        )
                        tp.solver_data.facts.append(new_fact)
                        new_fact.root_facts.add(find_fact_id_with_objects([polygon_2, polygon_1], 'relation'))
                        new_fact.description = 'из подобия многоугольников'

                        if new_fact.objects == actual_question.objects and new_fact.fact_type == actual_question.fact_type:
                            return True

                for k in range(len(polygon_1.points)):
                    ang_1 = tp.find_angle_with_points(polygon_1.points[k].name, polygon_1.points[k - 1].name, polygon_1.points[k - 2].name, tp.solver_data)
                    ang_2 = tp.find_angle_with_points(polygon_2.points[k].name, polygon_2.points[k - 1].name, polygon_2.points[k - 2].name, tp.solver_data)

                    try:
                        ang_1.relations[ang_2]

                    except KeyError:
                        ang_1.relations[ang_2] = Size(1)

                        new_fact = tp.Fact(
                            len(tp.solver_data.facts),
                            facts_generation,
                            'relation',
                            [ang_1, ang_2],
                            Size(1)
                        )
                        tp.solver_data.facts.append(new_fact)
                        new_fact.root_facts.add(find_fact_id_with_objects([polygon_1, polygon_2], 'relation'))
                        new_fact.description = 'из подобия многоугольников'

                        if new_fact.objects == actual_question.objects and new_fact.fact_type == actual_question.fact_type:
                            return True

                    try:
                        ang_2.relations[ang_1]

                    except KeyError:
                        ang_2.relations[ang_1] = Size(1)

                        new_fact = tp.Fact(
                            len(tp.solver_data.facts),
                            facts_generation,
                            'relation',
                            [ang_2, ang_1],
                            Size(1)
                        )
                        tp.solver_data.facts.append(new_fact)
                        new_fact.root_facts.add(find_fact_id_with_objects([polygon_2, polygon_1], 'relation'))
                        new_fact.description = 'из подобия многоугольников'

                        if new_fact.objects == actual_question.objects and new_fact.fact_type == actual_question.fact_type:
                            return True


def find_simmilar_triangles(facts_generation, actual_question):
    triangles = list(permutations(tp.solver_data.points, 3))

    for i in range(len(triangles)):
        for j in range(len(triangles)):
            if i != j:
                tr1 = tp.find_polygon_with_points(tp.get_points_names_from_list(triangles[i]), tp.solver_data)
                tr2 = tp.find_polygon_with_points(tp.get_points_names_from_list(triangles[j]), tp.solver_data)

                try:
                    tr1.relations[tr2]

                except KeyError:
                    A, B, C = tp.get_points_names_from_list(triangles[i])
                    D, E, F = tp.get_points_names_from_list(triangles[j])

                    seg11 = tp.find_segment_with_points(C, A, tp.solver_data)
                    seg12 = tp.find_segment_with_points(A, B, tp.solver_data)
                    seg13 = tp.find_segment_with_points(B, C, tp.solver_data)
                    seg21 = tp.find_segment_with_points(F, D, tp.solver_data)
                    seg22 = tp.find_segment_with_points(D, E, tp.solver_data)
                    seg23 = tp.find_segment_with_points(E, F, tp.solver_data)

                    ang11 = tp.find_angle_with_points(A, B, C, tp.solver_data)
                    ang12 = tp.find_angle_with_points(B, C, A, tp.solver_data)
                    ang13 = tp.find_angle_with_points(C, A, B, tp.solver_data)
                    ang21 = tp.find_angle_with_points(D, E, F, tp.solver_data)
                    ang22 = tp.find_angle_with_points(E, F, D, tp.solver_data)
                    ang23 = tp.find_angle_with_points(F, D, E, tp.solver_data)

                    segments_list_1 = [seg11, seg12, seg13]
                    segments_list_2 = [seg21, seg22, seg23]
                    angles_list_1 = [ang11, ang12, ang13]
                    angles_list_2 = [ang21, ang22, ang23]

                    simmilar_fact_1 = tp.Fact(
                        None,
                        facts_generation,
                        'relation',
                        [tr1, tr2],
                        None
                    )

                    # simmilar_fact_2 = tp.Fact(
                    #     None,
                    #     facts_generation,
                    #     'relation',
                    #     [tr2, tr1],
                    #     None
                    # )

                    # проверка подобия по углу и сторонам рядом с ним
                    for k in range(3):
                        try:
                            angles_relation = angles_list_1[k].size / angles_list_2[k].size
                        except TypeError:
                            try:
                                angles_relation = tp.solver_data.facts[
                                    find_fact_id_with_objects([angles_list_1[k], angles_list_2[k]], 'relation', None, Size(1))].value
                            except TypeError:
                                angles_relation = None

                        if angles_relation == Size(1):
                            if not angles_list_1[k].size or angles_list_1[k].size < 180:
                                try:
                                    first_segments_relation = segments_list_1[k - 1].size / segments_list_2[k - 1].size
                                except TypeError:
                                    try:
                                        first_segments_relation = tp.solver_data.facts[
                                            find_fact_id_with_objects([segments_list_1[k - 1], segments_list_2[k - 1]], 'relation')].value
                                    except TypeError:
                                        first_segments_relation = None

                                try:
                                    second_segments_relation = segments_list_1[k - 2].size / segments_list_2[k - 2].size
                                except TypeError:
                                    try:
                                        second_segments_relation = tp.solver_data.facts[
                                            find_fact_id_with_objects([segments_list_1[k - 2], segments_list_2[k - 2]], 'relation')].value
                                    except TypeError:
                                        second_segments_relation = None

                                if first_segments_relation and first_segments_relation == second_segments_relation:
                                    tr1.relations[tr2] = first_segments_relation
                                    # tr2.relations[tr1] = 1 / tp.solver_data.facts[first_angles_relation].value

                                    simmilar_fact_1.value = first_segments_relation
                                    simmilar_fact_1.root_facts.add(create_fact_about_objects_relations(
                                        [angles_list_1[k], angles_list_2[k]], facts_generation))
                                    simmilar_fact_1.root_facts.add(create_fact_about_objects_relations(
                                        [segments_list_1[k - 1], segments_list_2[k - 1]], facts_generation))
                                    simmilar_fact_1.root_facts.add(create_fact_about_objects_relations(
                                        [segments_list_1[k - 2], segments_list_2[k - 2]], facts_generation))
                                    simmilar_fact_1.description = 'по первому признаку подобия'
                                    simmilar_fact_1.id = len(tp.solver_data.facts)
                                    tp.solver_data.facts.append(simmilar_fact_1)

                                    if simmilar_fact_1.objects == actual_question.objects and simmilar_fact_1.fact_type == actual_question.fact_type:
                                        return True

                                    # simmilar_fact_2.value = 1 / tp.solver_data.facts[first_angles_relation].value
                                    # simmilar_fact_2.root_facts.add(first_angles_relation)
                                    # simmilar_fact_2.root_facts.add(second_angles_relation)
                                    # simmilar_fact_2.root_facts.add(segments_relation)
                                    # simmilar_fact_2.id = len(tp.solver_data.facts)
                                    # tp.solver_data.facts.append(simmilar_fact_2)

                                    continue

                    # проверка подобия по стороне и углам рядом с ним
                    for k in range(3):
                        try:
                            segments_relation = segments_list_1[k].size / segments_list_2[k].size
                        except TypeError:
                            try:
                                segments_relation = tp.solver_data.facts[
                                    find_fact_id_with_objects([segments_list_1[k], segments_list_2[k]], 'relation')].value
                            except TypeError:
                                segments_relation = None

                        if segments_relation:
                            try:
                                first_angles_relation = angles_list_1[k - 1].size / angles_list_2[k - 1].size
                            except TypeError:
                                try:
                                    first_angles_relation = tp.solver_data.facts[
                                        find_fact_id_with_objects([angles_list_1[k - 1], angles_list_2[k - 1]],
                                                                  'relation', None, Size(1))].value
                                except TypeError:
                                    first_angles_relation = None

                            try:
                                second_angles_relation = angles_list_1[k - 2].size / angles_list_2[k - 2].size
                            except TypeError:
                                try:
                                    second_angles_relation = tp.solver_data.facts[
                                        find_fact_id_with_objects([angles_list_1[k - 2], angles_list_2[k - 2]],
                                                                  'relation', None, Size(1))].value
                                except TypeError:
                                    second_angles_relation = None

                            if first_angles_relation == second_angles_relation == Size(1):
                                if (not angles_list_1[k - 1].size or angles_list_1[k - 1].size < 180) and (
                                        not angles_list_1[k - 2].size or angles_list_1[k - 2].size < 180):
                                    tr1.relations[tr2] = segments_relation
                                    # tr2.relations[tr1] = 1 / tp.solver_data.facts[first_angles_relation].value

                                    simmilar_fact_1.value = segments_relation
                                    simmilar_fact_1.root_facts.add(create_fact_about_objects_relations(
                                        [angles_list_1[k - 1], angles_list_2[k - 1]], facts_generation))
                                    simmilar_fact_1.root_facts.add(create_fact_about_objects_relations(
                                        [angles_list_1[k - 2], angles_list_2[k - 2]], facts_generation))
                                    simmilar_fact_1.root_facts.add(create_fact_about_objects_relations(
                                        [segments_list_1[k], segments_list_2[k]], facts_generation))
                                    simmilar_fact_1.description = 'по второму признаку подобия'
                                    simmilar_fact_1.id = len(tp.solver_data.facts)
                                    tp.solver_data.facts.append(simmilar_fact_1)

                                    if simmilar_fact_1.objects == actual_question.objects and simmilar_fact_1.fact_type == actual_question.fact_type:
                                        return True

                                    # simmilar_fact_2.value = 1 / tp.solver_data.facts[first_angles_relation].value
                                    # simmilar_fact_2.root_facts.add(first_angles_relation)
                                    # simmilar_fact_2.root_facts.add(second_angles_relation)
                                    # simmilar_fact_2.root_facts.add(segments_relation)
                                    # simmilar_fact_2.id = len(tp.solver_data.facts)
                                    # tp.solver_data.facts.append(simmilar_fact_2)

                                    continue

                    # проверка подобия по 3 сторонам
                    try:
                        first_segments_relation = seg11.size / seg21.size
                    except TypeError:
                        try:
                            first_segments_relation = tp.solver_data.facts[find_fact_id_with_objects([seg11, seg21], 'relation')].value
                        except TypeError:
                            continue

                    try:
                        second_segments_relation = seg12.size / seg22.size
                    except TypeError:
                        try:
                            second_segments_relation = tp.solver_data.facts[find_fact_id_with_objects([seg12, seg22], 'relation')].value
                        except TypeError:
                            continue

                    try:
                        third_segments_relation = seg13.size / seg23.size
                    except TypeError:
                        try:
                            third_segments_relation = tp.solver_data.facts[find_fact_id_with_objects([seg13, seg23], 'relation')].value
                        except TypeError:
                            continue

                    if first_segments_relation == second_segments_relation == third_segments_relation:
                        tr1.relations[tr2] = first_segments_relation
                        # tr2.relations[tr1] = 1 / tp.solver_data.facts[first_segments_relation].value

                        simmilar_fact_1.value = first_segments_relation
                        simmilar_fact_1.root_facts.add(
                            create_fact_about_objects_relations([seg11, seg21], facts_generation))
                        simmilar_fact_1.root_facts.add(
                            create_fact_about_objects_relations([seg12, seg22], facts_generation))
                        simmilar_fact_1.root_facts.add(
                            create_fact_about_objects_relations([seg13, seg23], facts_generation))
                        simmilar_fact_1.description = 'по третьему признаку подобия'
                        simmilar_fact_1.id = len(tp.solver_data.facts)
                        tp.solver_data.facts.append(simmilar_fact_1)

                        if simmilar_fact_1.objects == actual_question.objects and simmilar_fact_1.fact_type == actual_question.fact_type:
                            return True

                        # simmilar_fact_2.value = 1 / tp.solver_data.facts[first_segments_relation].value
                        # simmilar_fact_2.root_facts.add(first_segments_relation)
                        # simmilar_fact_2.root_facts.add(second_segments_relation)
                        # simmilar_fact_2.root_facts.add(third_segments_relation)
                        # simmilar_fact_2.id = len(tp.solver_data.facts)
                        # tp.solver_data.facts.append(simmilar_fact_2)

                        continue


def create_fact_about_objects_relations(objects, facts_generation):
    ans1 = find_fact_id_with_objects(objects, 'relation')
    ans2 = find_fact_id_with_objects([objects[1], objects[0]], 'relation')

    if not ans1 and not ans2:
        if objects[0].size and objects[1].size:
            simmilar_fact = tp.Fact(
                    len(tp.solver_data.facts),
                    facts_generation,
                    'relation',
                    [objects[0], objects[1]],
                    objects[0].size / objects[1].size
                )
            tp.solver_data.facts.append(simmilar_fact)
            simmilar_fact.root_facts.add(find_fact_id_with_objects([objects[0]], 'size'))
            simmilar_fact.root_facts.add(find_fact_id_with_objects([objects[1]], 'size'))

            return len(tp.solver_data.facts) - 1

        return None

    if ans1:
        return ans1

    return ans2


def find_fact_id_with_objects(objects, fact_type, facts_generation=None, value=None):
    for fact in tp.solver_data.facts:
        if objects == fact.objects:
            if not fact_type:
                if not value:
                    return fact.id
                if value == fact.value:
                    return fact.id
            if fact_type == fact.fact_type:
                if not value:
                    return fact.id
                if value == fact.value:
                    return fact.id

    if facts_generation.__class__.__name__ == 'int':
        tp.solver_data.facts.append(tp.Fact(
            len(tp.solver_data.facts),
            facts_generation,
            fact_type,
            objects,
            value
        ))
        return len(tp.solver_data.facts) - 1

    return None


def find_new_angles_in_triangles(facts_generation, actual_question):
    for triangle in combinations(tp.solver_data.points, 3):
        try_find_equal_sides = False
        A, B, C = triangle

        A = A.name
        B = B.name
        C = C.name

        seg_1 = tp.find_segment_with_points(C, A, tp.solver_data)
        seg_2 = tp.find_segment_with_points(A, B, tp.solver_data)
        seg_3 = tp.find_segment_with_points(B, C, tp.solver_data)

        ang_1 = tp.find_angle_with_points(*tp.check_angle_in_polygon(A, B, C, tp.solver_data), tp.solver_data)
        ang_2 = tp.find_angle_with_points(*tp.check_angle_in_polygon(B, C, A, tp.solver_data), tp.solver_data)
        ang_3 = tp.find_angle_with_points(*tp.check_angle_in_polygon(C, A, B, tp.solver_data), tp.solver_data)

        segments = [seg_1, seg_2, seg_3]
        angles = [ang_1, ang_2, ang_3]

        for i in range(3):
            if angles[i].size == 90:
                if not segments[i].size and segments[i - 1].size and segments[i - 2].size:
                    segments[i].size = sqrt(segments[i - 1].size ** 2 + segments[i - 2].size ** 2)
                    pythagoras_fact = tp.Fact(
                        len(tp.solver_data.facts),
                        facts_generation,
                        'size',
                        [segments[i]],
                        segments[i].size
                    )
                    tp.solver_data.facts.append(pythagoras_fact)
                    pythagoras_fact.root_facts.add(find_fact_id_with_objects([segments[i - 1]], 'size'))
                    pythagoras_fact.root_facts.add(find_fact_id_with_objects([segments[i - 2]], 'size'))
                    pythagoras_fact.root_facts.add(find_fact_id_with_objects([angles[i]], 'size'))
                    pythagoras_fact.description = 'по теореме Пифагора'

                    if pythagoras_fact.objects == actual_question.objects and pythagoras_fact.fact_type == actual_question.fact_type:
                        return True

                if not segments[i - 1].size and segments[i].size and segments[i - 2].size:
                    segments[i - 1].size = sqrt(segments[i].size ** 2 - segments[i - 2].size ** 2)
                    pythagoras_fact = tp.Fact(
                        len(tp.solver_data.facts),
                        facts_generation,
                        'size',
                        [segments[i - 1]],
                        segments[i - 1].size
                    )
                    tp.solver_data.facts.append(pythagoras_fact)
                    pythagoras_fact.root_facts.add(find_fact_id_with_objects([segments[i]], 'size'))
                    pythagoras_fact.root_facts.add(find_fact_id_with_objects([segments[i - 2]], 'size'))
                    pythagoras_fact.root_facts.add(find_fact_id_with_objects([angles[i]], 'size'))
                    pythagoras_fact.description = 'по теореме Пифагора'

                    if pythagoras_fact.objects == actual_question.objects and pythagoras_fact.fact_type == actual_question.fact_type:
                        return True

                if not segments[i - 2].size and segments[i].size and segments[i - 1].size:
                    segments[i - 2].size = sqrt(segments[i].size ** 2 - segments[i - 1].size ** 2)
                    pythagoras_fact = tp.Fact(
                        len(tp.solver_data.facts),
                        facts_generation,
                        'size',
                        [segments[i - 2]],
                        segments[i - 2].size
                    )
                    tp.solver_data.facts.append(pythagoras_fact)
                    pythagoras_fact.root_facts.add(find_fact_id_with_objects([segments[i - 1]], 'size'))
                    pythagoras_fact.root_facts.add(find_fact_id_with_objects([segments[i]], 'size'))
                    pythagoras_fact.root_facts.add(find_fact_id_with_objects([angles[i]], 'size'))
                    pythagoras_fact.description = 'по теореме Пифагора'

                    if pythagoras_fact.objects == actual_question.objects and pythagoras_fact.fact_type == actual_question.fact_type:
                        return True

                break

        else:
            if seg_1.size and seg_2.size and seg_3.size:
                for i in range(3):
                    if not angles[i].size and abs(segments[i].size ** 2 - segments[i - 1].size ** 2 - segments[i - 2].size ** 2) < 0.001:
                        angles[i].size = 90
                        back_pythagoras_fact = tp.Fact(
                            len(tp.solver_data.facts),
                            facts_generation,
                            'size',
                            [angles[i]],
                            90
                        )
                        tp.solver_data.facts.append(back_pythagoras_fact)
                        back_pythagoras_fact.root_facts.add(find_fact_id_with_objects([segments[i]], 'size'))
                        back_pythagoras_fact.root_facts.add(find_fact_id_with_objects([segments[i - 1]], 'size'))
                        back_pythagoras_fact.root_facts.add(find_fact_id_with_objects([segments[i - 2]], 'size'))
                        back_pythagoras_fact.description = 'по обратной теореме Пифагора'

                        if back_pythagoras_fact.objects == actual_question.objects and back_pythagoras_fact.fact_type == actual_question.fact_type:
                            return True

                        break

        for i in range(3):
            if (segments[i].size and segments[i - 1].size and segments[i].size == segments[
                i - 1].size) or find_fact_id_with_objects([segments[i], segments[i - 1]], 'relation', None,
                                                          Size(1)) or find_fact_id_with_objects(
                    [segments[i - 1], segments[i]], 'relation', None, Size(1)):
                try:
                    angles[i].relations[angles[i - 1]]
                except KeyError:
                    angles[i].relations[angles[i - 1]] = Size(1)
                    angles_equal_fact_1 = tp.Fact(
                        len(tp.solver_data.facts),
                        facts_generation,
                        'relation',
                        [angles[i], angles[i - 1]],
                        Size(1)
                    )
                    tp.solver_data.facts.append(angles_equal_fact_1)
                    angles_equal_fact_1.root_facts.add(create_fact_about_objects_relations([segments[i], segments[i - 1]], facts_generation))
                    angles_equal_fact_1.description = 'из равенства сторон в равнобедренном треугольнике'

                    if angles_equal_fact_1.objects == actual_question.objects and angles_equal_fact_1.fact_type == actual_question.fact_type:
                        return True

                try:
                    angles[i - 1].relations[angles[i]]
                except KeyError:
                    angles[i - 1].relations[angles[i]] = Size(1)
                    angles_equal_fact_2 = tp.Fact(
                        len(tp.solver_data.facts),
                        facts_generation,
                        'relation',
                        [angles[i - 1], angles[i]],
                        Size(1)
                    )
                    tp.solver_data.facts.append(angles_equal_fact_2)
                    angles_equal_fact_2.root_facts.add(create_fact_about_objects_relations([segments[i - 1], segments[i]], facts_generation))
                    angles_equal_fact_2.description = 'из равенства сторон в равнобедренном треугольнике'

                    if angles_equal_fact_2.objects == actual_question.objects and angles_equal_fact_2.fact_type == actual_question.fact_type:
                        return True

        if [ang_1.size, ang_2.size, ang_3.size].count(None) == 1:
            for i in range(3):
                if angles[i - 2].size and angles[i - 1].size and not angles[i].size:
                    angles[i].size = Size('180') - angles[i - 1].size - angles[i - 2].size

                    third_angle_size_fact = tp.Fact(
                        len(tp.solver_data.facts),
                        facts_generation,
                        'size',
                        [angles[i]],
                        angles[i].size
                    )
                    tp.solver_data.facts.append(third_angle_size_fact)
                    third_angle_size_fact.root_facts.add(find_fact_id_with_objects([angles[i - 1]], 'size'))
                    third_angle_size_fact.root_facts.add(find_fact_id_with_objects([angles[i - 2]], 'size'))
                    third_angle_size_fact.root_facts.add(
                        find_fact_id_with_objects({ang_1, ang_2, ang_3}, 'addition', facts_generation, Size(180)))
                    # third_angle_size_fact.description = 'из суммы углов в треугольнике 180'

                    if third_angle_size_fact.objects == actual_question.objects and third_angle_size_fact.fact_type == actual_question.fact_type:
                        return True

                    try_find_equal_sides = True

                    break

        if [ang_1.size, ang_2.size, ang_3.size].count(None) == 2:
            for i in range(3):
                if not angles[i - 2].size and not angles[i - 1].size and angles[i].size:
                    try:
                        rel = angles[i - 1].relations[angles[i - 2]]

                        angles[i - 1].size = (Size(180) - angles[i].size) / (1 + rel)
                        # angles[i - 2].size = angles[i - 1].size * rel

                        third_angle_size_fact = tp.Fact(
                            len(tp.solver_data.facts),
                            facts_generation,
                            'size',
                            [angles[i - 1]],
                            angles[i - 1].size
                        )
                        tp.solver_data.facts.append(third_angle_size_fact)
                        third_angle_size_fact.root_facts.add(
                            find_fact_id_with_objects([angles[i - 1], angles[i - 2]], 'relation'))
                        third_angle_size_fact.root_facts.add(
                            find_fact_id_with_objects({ang_1, ang_2, ang_3}, 'addition', facts_generation, Size(180)))
                        # third_angle_size_fact.description = 'из суммы углов в треугольнике 180'

                        try_find_equal_sides = True

                        if third_angle_size_fact.objects == actual_question.objects and third_angle_size_fact.fact_type == actual_question.fact_type:
                            return True

                        break

                    except KeyError:
                        pass

        if try_find_equal_sides:
            for i in range(3):
                if angles[i].size == angles[i - 1].size or find_fact_id_with_objects([angles[i], angles[i - 1]],
                                                                                     'relation', None, Size(
                                1)) or find_fact_id_with_objects([angles[i - 1], angles[i]], 'relation', None,
                                                                 Size(1)):
                    segments[i].relations[segments[i - 1]] = Size(1)
                    segments[i - 1].relations[segments[i]] = Size(1)

                    sides_equal_fact_1 = tp.Fact(
                        len(tp.solver_data.facts),
                        facts_generation,
                        'relation',
                        [segments[i], segments[i - 1]],
                        Size(1)
                    )
                    tp.solver_data.facts.append(sides_equal_fact_1)
                    sides_equal_fact_1.root_facts.add(
                        create_fact_about_objects_relations([angles[i], angles[i - 1]], facts_generation))
                    sides_equal_fact_1.description = 'из равенства углов в равнобедренном треугольнике'

                    if sides_equal_fact_1.objects == actual_question.objects and sides_equal_fact_1.fact_type == actual_question.fact_type:
                        return True

                    sides_equal_fact_2 = tp.Fact(
                        len(tp.solver_data.facts),
                        facts_generation,
                        'relation',
                        [segments[i - 1], segments[i]],
                        Size(1)
                    )
                    tp.solver_data.facts.append(sides_equal_fact_2)
                    sides_equal_fact_2.root_facts.add(
                        create_fact_about_objects_relations([angles[i - 1], angles[i]], facts_generation))
                    sides_equal_fact_2.description = 'из равенства углов в равнобедренном треугольнике'

                    if sides_equal_fact_2.objects == actual_question.objects and sides_equal_fact_2.fact_type == actual_question.fact_type:
                        return True


def create_null_facts_generation():
    for seg in tp.solver_data.segments:
        if seg.size:
            tp.solver_data.facts.append(tp.Fact(
                len(tp.solver_data.facts),
                0,
                'size',
                [seg],
                seg.size
            ))
        for rel_seg in seg.relations:
            tp.solver_data.facts.append(tp.Fact(
                len(tp.solver_data.facts),
                0,
                'relation',
                [seg, rel_seg],
                seg.relations[rel_seg]
            ))
        for dif_seg in seg.difference:
            tp.solver_data.facts.append(tp.Fact(
                len(tp.solver_data.facts),
                0,
                'difference',
                [seg, dif_seg],
                seg.difference[dif_seg]
            ))
        for add_seg in seg.addition:
            tp.solver_data.facts.append(tp.Fact(
                len(tp.solver_data.facts),
                0,
                'addition',
                {seg, add_seg},
                seg.addition[add_seg]
            ))

    for ang in tp.solver_data.angles:
        if ang.size:
            tp.solver_data.facts.append(tp.Fact(
                len(tp.solver_data.facts),
                0,
                'size',
                [ang],
                ang.size
            ))
        for rel_ang in ang.relations:
            tp.solver_data.facts.append(tp.Fact(
                len(tp.solver_data.facts),
                0,
                'relation',
                [ang, rel_ang],
                ang.relations[rel_ang]
            ))
        for dif_ang in ang.difference:
            tp.solver_data.facts.append(tp.Fact(
                len(tp.solver_data.facts),
                0,
                'difference',
                [ang, dif_ang],
                ang.difference[dif_ang]
            ))
        for add_ang in ang.addition:
            tp.solver_data.facts.append(tp.Fact(
                len(tp.solver_data.facts),
                0,
                'addition',
                {ang, add_ang},
                ang.addition[add_ang]
            ))

    # for i in range(len(tp.solver_data.segments) - 1):
    #     for j in range(i + 1, len(tp.solver_data.segments)):
    #         if tp.solver_data.segments[i].size and tp.solver_data.segments[j].size:
    #             find_fact_id_with_objects([tp.solver_data.segments[i], tp.solver_data.segments[j]], 'relation',
    #                                       tp.solver_data.segments[i].size / tp.solver_data.segments[j].size, 0)
    #             find_fact_id_with_objects([tp.solver_data.segments[j], tp.solver_data.segments[i]], 'relation',
    #                                       tp.solver_data.segments[j].size / tp.solver_data.segments[i].size, 0)
    #
    # for i in range(len(tp.solver_data.angles) - 1):
    #     for j in range(i + 1, len(tp.solver_data.angles)):
    #         if tp.solver_data.angles[i].size and tp.solver_data.angles[j].size:
    #             find_fact_id_with_objects([tp.solver_data.angles[i], tp.solver_data.angles[j]], 'relation',
    #                                       tp.solver_data.angles[i].size / tp.solver_data.angles[j].size, 0)
    #             find_fact_id_with_objects([tp.solver_data.angles[j], tp.solver_data.angles[i]], 'relation',
    #                                       tp.solver_data.angles[j].size / tp.solver_data.angles[i].size, 0)

    for pol in tp.solver_data.polygons:
        for rel_pol in pol.relations:
            tp.solver_data.facts.append(tp.Fact(
                len(tp.solver_data.facts),
                0,
                'relation',
                [pol, rel_pol],
                pol.relations[rel_pol]
            ))


def create_answer_tree(fact, tree, tree_levels, level=0):
    try:
        tree_levels[level]
    except IndexError:
        tree_levels.append(set())
    tree_levels[level].add(fact)

    if fact.root_facts:
        for root_fact_id in fact.root_facts:
            tree[tp.solver_data.facts[root_fact_id]] = dict()
            create_answer_tree(tp.solver_data.facts[root_fact_id], tree[tp.solver_data.facts[root_fact_id]], tree_levels, level + 1)


def tree_levels_proccesing(tree_levels):
    ret = list()
    for level in reversed(tree_levels):
        ret += list(level)

    return ret


def solving_process():
    facts_generation = 1
    solutions = dict()

    create_null_facts_generation()

    for question in tp.solver_data.questions:
        facts_list_length = len(tp.solver_data.facts)
        while not find_fact_id_with_objects(question.objects, question.fact_type):
            if count_sizes_of_angles_and_segments(tp.solver_data.segments, facts_generation, question):
                break
            if count_sizes_of_angles_and_segments(tp.solver_data.angles, facts_generation, question):
                break
            if find_new_angles_in_triangles(facts_generation, question):
                break
            if find_simmilar_triangles(facts_generation, question):
                break
            if count_sides_and_angles_of_similar_polygons(facts_generation, question):
                break
            if facts_list_length == len(tp.solver_data.facts):
                break

            facts_list_length = len(tp.solver_data.facts)
            facts_generation += 1

        # for fact in tp.solver_data.facts:
        #     print(fact)
        # print()

        try:
            question_fact = tp.solver_data.facts[find_fact_id_with_objects(question.objects, question.fact_type)]
            solution_tree = {question_fact: dict()}
            solution_tree_levels = list()
            create_answer_tree(question_fact, solution_tree[question_fact], solution_tree_levels)
            solutions[question] = {'tree': solution_tree, 'tree_levels': solution_tree_levels}

        except TypeError:
            solutions[question] = {'tree': {}, 'tree_levels': []}

    return {'facts': solutions, 'data': tp.solver_data}
