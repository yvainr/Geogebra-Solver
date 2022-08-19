import task_parser as tp
from random import choice


def pretty_name(obj, dative=False, genitive=False):
    if obj.__class__.__name__ == 'Segment':
        A, B = obj.points
        if dative:
            return f'отрезку {A.name}{B.name}'
        if genitive:
            return f'отрезка {A.name}{B.name}'
        return f'отрезок {A.name}{B.name}'

    if obj.__class__.__name__ == 'Angle':
        A = list(obj.rays[0].points)[0]
        B = obj.rays[0].main_point
        C = list(obj.rays[1].points)[0]
        # if dative:
        #     return f'углу {A.name}{B.name}{C.name}'
        # if genitive:
        #     return f'угла {A.name}{B.name}{C.name}'
        # return f'угол {A.name}{B.name}{C.name}'
        return f'∠{A.name}{B.name}{C.name}'

    if obj.__class__.__name__ == 'Polygon':
        if dative:
            return f'многоугольнику {obj.name[8:]}'
        if genitive:
            return f'многоугольника {obj.name[8:]}'
        return f'многоугольник {obj.name[8:]}'


def pretty_description(fact, called=False):
    if fact.fact_type == 'size':
        answer = f'{pretty_name(fact.objects[0])} равен {fact.value.conversion_to_latex()}'
    if fact.fact_type == 'relation':
        if fact.value != 1:
            answer = f'{pretty_name(fact.objects[0])} подобен {pretty_name(fact.objects[1], True)} с коэффициентом {fact.value.conversion_to_latex()}'
        else:
            answer = f'{pretty_name(fact.objects[0])} равен {pretty_name(fact.objects[1], True)}'
    if fact.fact_type == 'difference':
        answer = f'разность {pretty_name(fact.objects[0], False, True)} и {pretty_name(fact.objects[1], False, True)} равна {fact.value.conversion_to_latex()}'
    if fact.fact_type == 'addition':
        answer = 'сумма '
        for obj in fact.objects:
            answer += f'{pretty_name(obj, False, True)}, '
        answer = answer[:-2] + f' равна {fact.value.conversion_to_latex()}'
        answer = answer[:answer.rfind(',')] + ' и' + answer[answer.rfind(',') + 1:]

    if called:
        return answer

    if fact.description:
        answer = f'{fact.description} {answer}'
    return answer[0].upper() + answer[1:] + '.'


def pretty_detailed_description(fact):
    if fact.generation:
        if fact.root_facts:
            answer = f'{pretty_description(fact, True)}, {choice(["потому что ", "так как ", "поскольку "])}'
            if len(fact.root_facts) > 1:
                for i in range(len(fact.root_facts) - 1):
                    answer += f'{pretty_description(tp.solver_data.facts[list(fact.root_facts)[i]], True)}, '
                answer = answer[:-2] + f' и {pretty_description(tp.solver_data.facts[list(fact.root_facts)[-1]], True)}'
            else:
                answer += f'{pretty_description(tp.solver_data.facts[list(fact.root_facts)[0]], True)}'
        else:
            answer = pretty_description(fact, True)
    else:
        answer = f'{pretty_description(fact, True)} из условия'

    if fact.description:
        answer = f'{fact.description} {answer}'

    return answer[0].upper() + answer[1:] + '.'


def pretty_question(question):
    if not question.value:
        if question.fact_type == 'size':
            answer = f'Найти величину {pretty_name(question.objects[0], False, True)}'
        if question.fact_type == 'relation':
            answer = f'Найти отношение {pretty_name(question.objects[0], False, True)} к {pretty_name(question.objects[1], True)}'
        if question.fact_type == 'difference':
            answer = f'Найти разность {pretty_name(question.objects[0], False, True)} и {pretty_name(question.objects[1], False, True)}'
        if question.fact_type == 'addition':
            answer = f'Найти сумму '
            for obj in question.objects:
                answer += f'{pretty_name(obj, False, True)} ,'
            answer = answer[:-2]
            answer = answer[:answer.rfind(',')] + ' и' + answer[answer.rfind(',') + 1:]

        return answer + '.'
