from pprint import pprint
import multiprocessing

import Solver_alpha
import task_parser

from polygon_drawer import text_splitter
from language_interpreter import text_analyze
from updated_solver import solving_process
from datetime import datetime

BUTTON_TYPES = {'red':'danger', 'green':'success'}

RESHALKA = 'normal'
# RESHALKA = 'alpha'

def insert_test_facts():
    inp = text_analyze('Даны треугольники ABC, и DEF, AB = 5, DE = 5, BC = 3, EF = 3, угол CBA равен 90, угол FED равен 90\nДокажите, что треугольник ABC равен DEF ')
    pprint(inp)
    # inp = "ABC, DEF\nAB 5, DE 10\nABC 40, FED 40, BCA 50, EDF 90\n\n\n\n\n/ABC DEF ?"

    text_splitter(inp, input_file_name='templates/solving_template.html')



def get_dict_of_facts(return_dict, data):
    task_parser.solver_data = data
    solving_result = {}
    stat = datetime.now()
    print('SOLVING START')

    if RESHALKA == 'normal':
        solving_result = solving_process()  # Нормальная решалка
        print(solving_result)
    elif RESHALKA == 'alpha':
        solving_result = Solver_alpha.solving_process()  # решалка Ильи

    print(datetime.now() - stat, 'SOLVING FINISHED')

    iterated_facts = solving_result['facts']
    # print(iterated_facts)
    data = solving_result['data']
    # print(data)


    try:
        fact_key = list(iterated_facts.keys())[0]
    except IndexError:
        return {}

    return_dict['question fact'] = fact_key
    return_dict['list of reason facts'] = iterated_facts[fact_key]
    return_dict['data'] = data

    print(datetime.now() - stat, 'RETURNING RESULT')
    # print(return_dict)

    return return_dict


# insert_test_facts()
# if __name__ == "__main__":
#     manager = multiprocessing.Manager()
#     return_dict = manager.dict()
#     p = multiprocessing.Process(target=get_dict_of_facts, args=(return_dict,))
#     p.start()
#     p.join(5)
#     print(return_dict)
#     p.terminate()
    # exit()

# for i in range(5):
#     p = multiprocessing.Process(target=worker, args=(i, return_dict))
#     jobs.append(p)
#     p.start()
#
# for proc in jobs:
#     proc.join()
