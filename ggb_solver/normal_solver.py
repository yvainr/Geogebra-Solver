import ggb_data_processing.task_parser as tp
# import sys
from time import time
from itertools import combinations, permutations
from ggb_data_processing.objects_types import Size, sqrt
from pprint import pprint
# from fact_description.detailed_fact_description import pretty_detailed_description

# sys.setrecursionlimit(2000)


# на случай реорганизации набора фактов
def update_facts(fact_type, new_fact, actual_question, facts_generation):
    tp.solver_data.facts[fact_type].append(new_fact)
    if check_is_fact_answer(new_fact, actual_question, facts_generation):
        return True


def count_sizes_of_angles_and_segments(facts_generation, actual_question, iterations=2):
    for objects in [tp.solver_data.segments, tp.solver_data.angles]:
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

                        if check_is_fact_answer(double_simmilar_fact, actual_question, facts_generation):
                            return True

    for n in range(iterations):
        for i in range(len(tp.solver_data.facts)):
            fact = tp.solver_data.facts[i]
            if fact.fact_type == 'relation' and fact.objects[0].__class__.__name__ != 'Polygon':
                if fact.objects[0].size and not fact.objects[1].size:
                    fact.objects[1].size = fact.objects[0].size / fact.value
                    size_fact = tp.Fact(
                        len(tp.solver_data.facts),
                        facts_generation,
                        'size',
                        [fact.objects[1]],
                        fact.objects[1].size
                    )
                    tp.solver_data.facts.append(size_fact)
                    size_fact.root_facts.add(i)
                    size_fact.root_facts.add(find_fact_id_with_objects([fact.objects[0]], 'size'))

                    if check_is_fact_answer(size_fact, actual_question, facts_generation):
                        return True

                elif fact.objects[1].size and not fact.objects[0].size:
                    fact.objects[0].size = fact.objects[1].size * fact.value
                    size_fact = tp.Fact(
                        len(tp.solver_data.facts),
                        facts_generation,
                        'size',
                        [fact.objects[0]],
                        fact.objects[0].size
                    )
                    tp.solver_data.facts.append(size_fact)
                    size_fact.root_facts.add(i)
                    size_fact.root_facts.add(find_fact_id_with_objects([fact.objects[1]], 'size'))

                    if check_is_fact_answer(size_fact, actual_question, facts_generation):
                        return True

            elif fact.fact_type == 'difference':
                if fact.objects[0].size and not fact.objects[1].size:
                    fact.objects[1].size = fact.objects[0].size - fact.value
                    size_fact = tp.Fact(
                        len(tp.solver_data.facts),
                        facts_generation,
                        'size',
                        [fact.objects[1]],
                        fact.objects[1].size
                    )
                    tp.solver_data.facts.append(size_fact)
                    size_fact.root_facts.add(i)
                    size_fact.root_facts.add(find_fact_id_with_objects([fact.objects[0]], 'size'))

                    if check_is_fact_answer(size_fact, actual_question, facts_generation):
                        return True

                elif fact.objects[1].size and not fact.objects[0].size:
                    fact.objects[0].size = fact.objects[1].size + fact.value
                    size_fact = tp.Fact(
                        len(tp.solver_data.facts),
                        facts_generation,
                        'size',
                        [fact.objects[0]],
                        fact.objects[0].size
                    )
                    tp.solver_data.facts.append(size_fact)
                    size_fact.root_facts.add(i)
                    size_fact.root_facts.add(find_fact_id_with_objects([fact.objects[1]], 'size'))

                    if check_is_fact_answer(size_fact, actual_question, facts_generation):
                        return True

            elif fact.fact_type == 'addition':
                real_sum = fact.value
                none_value_list = list()
                continue_find = True

                for obj in fact.objects:
                    if obj.size:
                        real_sum -= obj.size
                    else:
                        none_value_list.append(obj)

                for n_obj in none_value_list:
                    n_obj_relations = [1]

                    for obj in none_value_list:
                        if n_obj in obj.relations:
                            n_obj_relations.append(obj.relations[n_obj])

                    if len(n_obj_relations) == len(none_value_list):
                        n_obj.size = real_sum / sum(n_obj_relations)
                        size_fact = tp.Fact(
                            len(tp.solver_data.facts),
                            facts_generation,
                            'size',
                            [n_obj],
                            n_obj.size
                        )
                        tp.solver_data.facts.append(size_fact)
                        size_fact.root_facts.add(i)

                        for root_fact in fact.objects:
                            if root_fact != n_obj:
                                if root_fact.size:
                                    size_fact.root_facts.add(find_fact_id_with_objects([root_fact], 'size'))
                                else:
                                    size_fact.root_facts.add(find_fact_id_with_objects([n_obj, root_fact], 'relation'))

                        if check_is_fact_answer(size_fact, actual_question, facts_generation):
                            return True

                        continue_find = False
                        break

                if not continue_find:
                    break


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

                            if check_is_fact_answer(simmilar_fact, actual_question, facts_generation):
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

                            if check_is_fact_answer(simmilar_fact, actual_question, facts_generation):
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

                if check_is_fact_answer(simmilar_fact, actual_question, facts_generation):
                    return True

                if count_sides_and_angles_of_similar_triangles(facts_generation, actual_question, tr1, tr2,
                                                               segments_list_1, angles_list_1,
                                                               segments_list_2, angles_list_2):
                    return True

                return None


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

                if check_is_fact_answer(new_fact, actual_question, facts_generation):
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

                if check_is_fact_answer(new_fact, actual_question, facts_generation):
                    return True


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

                    if check_is_fact_answer(pythagoras_fact, actual_question, facts_generation):
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

                    if check_is_fact_answer(pythagoras_fact, actual_question, facts_generation):
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

                    if check_is_fact_answer(pythagoras_fact, actual_question, facts_generation):
                        return True

                break

        else:
            if segments[0].size and segments[1].size and segments[2].size:
                for i in range(3):
                    if not angles[i].size and abs(segments[i].size ** 2 - segments[i - 1].size ** 2 - segments[i - 2].size ** 2) < 0.001:
                        angles[i].size = Size(90)
                        back_pythagoras_fact = tp.Fact(
                            len(tp.solver_data.facts),
                            facts_generation,
                            'size',
                            [angles[i]],
                            Size(90)
                        )
                        tp.solver_data.facts.append(back_pythagoras_fact)
                        back_pythagoras_fact.root_facts.add(find_fact_id_with_objects([segments[i]], 'size'))
                        back_pythagoras_fact.root_facts.add(find_fact_id_with_objects([segments[i - 1]], 'size'))
                        back_pythagoras_fact.root_facts.add(find_fact_id_with_objects([segments[i - 2]], 'size'))
                        back_pythagoras_fact.description = 'по обратной теореме Пифагора'

                        if check_is_fact_answer(back_pythagoras_fact, actual_question, facts_generation):
                            return True

                        break

        for i in range(3):
            if (segments[i].size and segments[i - 1].size and segments[i].size == segments[
                i - 1].size) or find_fact_id_with_objects([segments[i], segments[i - 1]], 'relation', Size(1)) or \
                    find_fact_id_with_objects([segments[i - 1], segments[i]], 'relation', Size(1)):
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

                    if check_is_fact_answer(angles_equal_fact_1, actual_question, facts_generation):
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

                    if check_is_fact_answer(angles_equal_fact_2, actual_question, facts_generation):
                        return True

        for i in range(3):
            if (angles[i].size and angles[i - 1].size and angles[i].size == angles[
                i - 1].size) or find_fact_id_with_objects([angles[i], angles[i - 1]], 'relation',
                                                          Size(1)) or find_fact_id_with_objects(
                    [angles[i - 1], angles[i]], 'relation', Size(1)):
                try:
                    segments[i].relations[segments[i - 1]]
                except KeyError:
                    segments[i].relations[segments[i - 1]] = Size(1)
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

                    if check_is_fact_answer(sides_equal_fact_1, actual_question, facts_generation):
                        return True

                try:
                    segments[i - 1].relations[segments[i]]
                except KeyError:
                    segments[i - 1].relations[segments[i]] = Size(1)
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

                    if check_is_fact_answer(sides_equal_fact_2, actual_question, facts_generation):
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

    for triangle in combinations(tp.solver_data.points, 3):
        A, B, C = triangle
        if tp.find_segment_with_points(A.name, B.name, tp.solver_data, False) and tp.find_segment_with_points(B.name, C.name,
                                                                                                    tp.solver_data,
                                                                                                    False) and tp.find_segment_with_points(
                C.name, A.name, tp.solver_data, False):
            tp.solver_data.facts.append(tp.Fact(
                len(tp.solver_data.facts),
                0,
                'addition',
                set(tp.find_polygon_with_points([A.name, B.name, C.name]).angles),
                Size(180)
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


def check_is_fact_answer(fact, question, facts_generation):
    if question:
        if fact.objects == question.objects and fact.fact_type == question.fact_type:
            return True
        if fact.fact_type == 'size' and question.fact_type == 'relation' and fact.objects[0] in question.objects:
            if create_fact_about_objects_relations(question.objects, facts_generation):
                return True


def check_time(start_time, dead_time=10):
    return dead_time > (start_time - time())


def run_solve_functions(facts_generation, question, start_time):
    if not check_time(start_time):
        return 'INFO - solve time limit'
    if count_sizes_of_angles_and_segments(facts_generation, question):
        return 'INFO - answer finded in module 1'

    if not check_time(start_time):
        return 'INFO - solve time limit'
    if find_new_angles_in_triangles(facts_generation, question):
        return 'INFO - answer finded in module 2'

    if not check_time(start_time):
        return 'INFO - solve time limit'
    if find_simmilar_triangles(facts_generation, question) or not check_time(start_time):
        return 'INFO - answer finded in module 3'


def solving_process():
    solutions = dict()
    start_time = time()

    facts_generation = 0
    create_null_facts_generation()

    for question in tp.solver_data.questions:
        while True:
            facts_list_length = len(tp.solver_data.facts)
            facts_generation += 1
            first_check_stop = False

            for fact in tp.solver_data.facts:
                if check_is_fact_answer(fact, question, facts_generation):
                    first_check_stop = True
                    break

            if first_check_stop:
                break
            if run_solve_functions(facts_generation, question, start_time):
                break
            if facts_list_length == len(tp.solver_data.facts):
                break

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

    if not len(tp.solver_data.questions):
        run_solve_functions(facts_generation, None, start_time)

    return {'facts': solutions, 'data': tp.solver_data}
