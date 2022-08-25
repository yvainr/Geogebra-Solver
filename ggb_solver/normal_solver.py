import ggb_data_processing.task_parser as tp
# import sys
from itertools import combinations, permutations
from ggb_data_processing.objects_types import Size, sqrt

# sys.setrecursionlimit(2000)


# на случай реорганизации набора фактов
def update_facts(fact_type, new_fact, actual_question):
    tp.solver_data.facts[fact_type].append(new_fact)
    if new_fact.objects == actual_question.objects and fact_type == actual_question.fact_type:
        return True


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

                            if actual_question and new_fact.objects == actual_question.objects and new_fact.fact_type == actual_question.fact_type:
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

                                if actual_question and new_fact.objects == actual_question.objects and new_fact.fact_type == actual_question.fact_type:
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

                                    if actual_question and new_fact.objects == actual_question.objects and new_fact.fact_type == actual_question.fact_type:
                                        return True

                                except KeyError:
                                    pass

    for obj1 in objects:
        for obj2 in list(obj1.relations):
            for obj3 in obj2.relations:
                if obj3 not in obj1.relations and obj3 != obj1:
                    obj1.relations[obj3] = obj1.relations[obj2] * obj2.relations[obj3]
                    double_simmilar_fact = tp.Fact(
                        len(tp.solver_data.facts),
                        facts_generation,
                        'relation',
                        [obj1, obj3],
                        obj1.relations[obj3]
                    )
                    tp.solver_data.facts.append(double_simmilar_fact)
                    double_simmilar_fact.root_facts.add(find_fact_id_with_objects([obj1, obj2], 'relation'))
                    double_simmilar_fact.root_facts.add(find_fact_id_with_objects([obj2, obj3], 'relation'))

                    if double_simmilar_fact.objects == actual_question.objects and double_simmilar_fact.fact_type == actual_question.fact_type:
                        return True


def count_sides_and_angles_of_similar_triangles(facts_generation, actual_question, polygon_1, polygon_2,
                                                segments_list_1, angles_list_1, segments_list_2, angles_list_2):
    try:
        rel = polygon_1.relations[polygon_2]

    except KeyError:
        try:
            rel = 1 / polygon_2.relations[polygon_1]

        except KeyError:
            rel = None

    if rel:
        for k in range(3):
            seg_1 = segments_list_1[k]
            seg_2 = segments_list_2[k]

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

        for k in range(3):
            ang_1 = angles_list_1[k]
            ang_2 = angles_list_2[k]

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


def find_simmilar_triangles(facts_generation, actual_question):
    for triangle_couple in list(permutations(combinations(tp.solver_data.points, 3), 2)):
        tr1 = tp.find_polygon_with_points(tp.get_points_names_from_list(list(triangle_couple[0])))
        tr2 = tp.find_polygon_with_points(tp.get_points_names_from_list(list(triangle_couple[1])))

        try:
            tr1.relations[tr2]

        except KeyError:
            if check_is_triangles_simmilar(tr1, tr2, facts_generation, actual_question):
                return True


def check_is_triangles_simmilar(tr1, tr2, facts_generation, actual_question):
    segments_list_1 = tr1.sides
    angles_list_1 = tr1.angles

    for second_triangle_data in [[tr2.sides, tr2.angles], [tr2.sides[::-1], tr2.angles[::-1]]]:
        for shift in range(3):
            segments_list_2 = second_triangle_data[0][shift:] + second_triangle_data[0][:shift]
            angles_list_2 = second_triangle_data[1][shift:] + second_triangle_data[1][:shift]

            simmilar_fact = tp.Fact(
                None,
                facts_generation,
                'relation',
                [tr1, tr2],
                None
            )

            # проверка подобия по углу и сторонам рядом с ним
            for k in range(3):
                try:
                    angles_relation = angles_list_1[k].size / angles_list_2[k].size
                except TypeError:
                    try:
                        angles_relation = tp.solver_data.facts[
                            find_fact_id_with_objects([angles_list_1[k], angles_list_2[k]], 'relation', Size(1))].value
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

                            simmilar_fact.value = first_segments_relation
                            simmilar_fact.root_facts.add(create_fact_about_objects_relations(
                                [angles_list_1[k], angles_list_2[k]], facts_generation))
                            simmilar_fact.root_facts.add(create_fact_about_objects_relations(
                                [segments_list_1[k - 1], segments_list_2[k - 1]], facts_generation))
                            simmilar_fact.root_facts.add(create_fact_about_objects_relations(
                                [segments_list_1[k - 2], segments_list_2[k - 2]], facts_generation))
                            simmilar_fact.description = 'по первому признаку подобия'
                            simmilar_fact.id = len(tp.solver_data.facts)
                            tp.solver_data.facts.append(simmilar_fact)

                            if simmilar_fact.objects == actual_question.objects and simmilar_fact.fact_type == actual_question.fact_type:
                                return True

                            if count_sides_and_angles_of_similar_triangles(facts_generation, actual_question, tr1, tr2,
                                                                           segments_list_1, angles_list_1,
                                                                           segments_list_2, angles_list_2):
                                return True

                            return None

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
                                                          'relation', Size(1))].value
                        except TypeError:
                            first_angles_relation = None

                    try:
                        second_angles_relation = angles_list_1[k - 2].size / angles_list_2[k - 2].size
                    except TypeError:
                        try:
                            second_angles_relation = tp.solver_data.facts[
                                find_fact_id_with_objects([angles_list_1[k - 2], angles_list_2[k - 2]],
                                                          'relation', Size(1))].value
                        except TypeError:
                            second_angles_relation = None

                    if first_angles_relation == second_angles_relation == Size(1):
                        if (not angles_list_1[k - 1].size or angles_list_1[k - 1].size < 180) and (
                                not angles_list_1[k - 2].size or angles_list_1[k - 2].size < 180):
                            tr1.relations[tr2] = segments_relation

                            simmilar_fact.value = segments_relation
                            simmilar_fact.root_facts.add(create_fact_about_objects_relations(
                                [angles_list_1[k - 1], angles_list_2[k - 1]], facts_generation))
                            simmilar_fact.root_facts.add(create_fact_about_objects_relations(
                                [angles_list_1[k - 2], angles_list_2[k - 2]], facts_generation))
                            simmilar_fact.root_facts.add(create_fact_about_objects_relations(
                                [segments_list_1[k], segments_list_2[k]], facts_generation))
                            simmilar_fact.description = 'по второму признаку подобия'
                            simmilar_fact.id = len(tp.solver_data.facts)
                            tp.solver_data.facts.append(simmilar_fact)

                            if simmilar_fact.objects == actual_question.objects and simmilar_fact.fact_type == actual_question.fact_type:
                                return True

                            if count_sides_and_angles_of_similar_triangles(facts_generation, actual_question, tr1, tr2,
                                                                           segments_list_1, angles_list_1,
                                                                           segments_list_2, angles_list_2):
                                return True

                            return None

            # проверка подобия по 3 сторонам
            try:
                first_segments_relation = segments_list_1[0].size / segments_list_2[0].size
            except TypeError:
                try:
                    first_segments_relation = tp.solver_data.facts[find_fact_id_with_objects([segments_list_1[0], segments_list_2[0]], 'relation')].value
                except TypeError:
                    first_segments_relation = None

            try:
                second_segments_relation = segments_list_1[1].size / segments_list_2[1].size
            except TypeError:
                try:
                    second_segments_relation = tp.solver_data.facts[find_fact_id_with_objects([segments_list_1[1], segments_list_2[1]], 'relation')].value
                except TypeError:
                    second_segments_relation = None

            try:
                third_segments_relation = segments_list_1[2].size / segments_list_2[2].size
            except TypeError:
                try:
                    third_segments_relation = tp.solver_data.facts[find_fact_id_with_objects([segments_list_1[2], segments_list_2[2]], 'relation')].value
                except TypeError:
                    third_segments_relation = None

            if first_segments_relation and first_segments_relation == second_segments_relation == third_segments_relation:
                tr1.relations[tr2] = first_segments_relation

                simmilar_fact.value = first_segments_relation
                simmilar_fact.root_facts.add(
                    create_fact_about_objects_relations([segments_list_1[0], segments_list_2[0]], facts_generation))
                simmilar_fact.root_facts.add(
                    create_fact_about_objects_relations([segments_list_1[1], segments_list_2[1]], facts_generation))
                simmilar_fact.root_facts.add(
                    create_fact_about_objects_relations([segments_list_1[2], segments_list_2[2]], facts_generation))
                simmilar_fact.description = 'по третьему признаку подобия'
                simmilar_fact.id = len(tp.solver_data.facts)
                tp.solver_data.facts.append(simmilar_fact)

                if simmilar_fact.objects == actual_question.objects and simmilar_fact.fact_type == actual_question.fact_type:
                    return True

                if count_sides_and_angles_of_similar_triangles(facts_generation, actual_question, tr1, tr2,
                                                               segments_list_1, angles_list_1,
                                                               segments_list_2, angles_list_2):
                    return True

                return None


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


def find_fact_id_with_objects(objects, fact_type, value=None, facts_generation=None):
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
        tr = tp.find_polygon_with_points([A.name, B.name, C.name])

        segments = tr.sides
        angles = tr.angles

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
            if segments[0].size and segments[1].size and segments[2].size:
                for i in range(3):
                    if not angles[i].size and abs(segments[i].size ** 2 - segments[i - 1].size ** 2 - segments[i - 2].size ** 2) < 0.001:
                        angles[i].size = 90
                        back_pythagoras_fact = tp.Fact(
                            len(tp.solver_data.facts),
                            facts_generation,
                            'size',
                            [angles[i]],
                            Size('90')
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
                i - 1].size) or find_fact_id_with_objects([segments[i], segments[i - 1]], 'relation', Size(1)) or \
                    find_fact_id_with_objects([segments[i - 1], segments[i]], 'relation', None, Size(1)):
                try:
                    angles[i].relations[angles[i - 1]]
                except KeyError:
                    angles[i].relations[angles[i - 1]] = Size(1)
                    angles_equal_fact_1 = tp.Fact(
                        len(tp.solver_data.facts),
                        facts_generation,
                        'relation',
                        [angles[i], angles[i - 1]],
                        Size('1')
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

        if [angles[0].size, angles[1].size, angles[2].size].count(None) == 1:
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
                        find_fact_id_with_objects(set(angles), 'addition', Size(180), facts_generation))
                    # third_angle_size_fact.description = 'из суммы углов в треугольнике 180'

                    if third_angle_size_fact.objects == actual_question.objects and third_angle_size_fact.fact_type == actual_question.fact_type:
                        return True

                    try_find_equal_sides = True

                    break

        if [angles[0].size, angles[1].size, angles[2].size].count(None) == 2:
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
                            find_fact_id_with_objects({angles[i], angles[i - 1], angles[i - 2]}, 'addition', Size(180), facts_generation))
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
                                                                                     'relation',  Size(1)) \
                        or find_fact_id_with_objects([angles[i - 1], angles[i]], 'relation', Size(1)):
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


def tree_levels_processing(tree_levels):
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
        while True:
            if count_sizes_of_angles_and_segments(tp.solver_data.segments, facts_generation, question):
                break
            if count_sizes_of_angles_and_segments(tp.solver_data.angles, facts_generation, question):
                break
            if find_new_angles_in_triangles(facts_generation, question):
                break
            if find_simmilar_triangles(facts_generation, question):
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
            solutions[question] = {'tree': solution_tree, 'tree_levels': solution_tree_levels, 'errors': None}

        except TypeError:
            solutions[question] = {'tree': {}, 'tree_levels': [],
                                   'errors': 'Не смогли решить задачу. '
                                             'Проверьте корректность введенного условия, '
                                             'предварительно ознакомившись с инструкцией по вводу.'}

    return {'facts': solutions, 'data': tp.solver_data}
