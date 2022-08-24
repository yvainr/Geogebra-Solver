from flask import Flask, render_template, request, flash
import logging
import multiprocessing

from ggb_data_proccesing import task_parser, task_parser as taskp
from ggb_html_generator.geogebra_html_generator import insert_commands
from ggb_drawer.polygon_drawer import text_splitter
from ggb_text_proccesing.language_interpreter import text_analyze
from web_facts_tools import get_dict_of_facts, get_necessary_coords_size
# from Solver_alpha import to_str
from fact_description.short_fact_description import fact_output
from random import choice
from ggb_solver.normal_solver import tree_levels_proccesing
from fact_description.detailed_fact_description import pretty_detailed_description
# from normal_solver import solving_process

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO

)

logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='./templates',static_folder='./static')
app.config['SECRET_KEY'] = 'abcdef12345678'
app.config['TEMPLATES_AUTO_RELOAD'] = True

SOLVING_TIME_LIMIT = 30 #seconds

# app.jinja_env.globals.update(to_str=to_str)
app.jinja_env.globals.update(fact_output=fact_output)
app.jinja_env.globals.update(solution_interpreter=pretty_detailed_description)
app.jinja_env.globals.update(list=list)
app.jinja_env.globals.update(str=str)
app.jinja_env.globals.update(set=set)
app.jinja_env.globals.update(get_necessary_coords_size=get_necessary_coords_size)


def split_commands(commands_text: str):
    commands_list = commands_text.split('\n')  # разрезаем его на строки
    commands_list = [command.replace('\n', '').replace('\r', '') for command in commands_list]  # стираем в каждой строке \n
    commands_list = [command for command in commands_list if command]
    return commands_list

@app.route('/commands_input', methods=('GET', 'POST'))
def index(commands_text=''):
    logger.info('Commands input page requested')
    # if request.method == 'POST':
    commands_text = request.args.get('commands_text')
    logger.info(f'Commands: {commands_text}')
    # print(repr(commands_text))
    return render_template('index.html', commands_text=commands_text)

@app.route('/', methods=('GET', 'POST'))
def text_input(text='', commands_text=''):
    logger.info('Text input page requested')
    # if request.method == 'POST':
    text = request.args.get('text')
    commands_text = request.args.get('commands_text')

    logger.info(f'Text:{text}')
    logger.info(f'Text commads:\n{commands_text}')

    with open('static/quotes.txt', 'r') as fin:
        quotes = fin.read()

    quotes = quotes.split('*')

    quote = choice(quotes)

    # print(repr(commands_text))
    return render_template('input.html', text=text, commands_text=commands_text, quote=quote)

@app.route('/render_geogebra', methods=('GET', 'POST'))
def create():
    logger.info('Render page requested')
    if request.method == 'POST':
        commands_text = request.form['commands']

        if not commands_text:
            logger.info('flashed')
            flash('Commands are required!')

        else:
            commands = split_commands(commands_text)

            logger.info(f'Recieved geogebra commands: {commands}')

            insert_commands(commands, input_file_name='templates/drawing_template.html', output_file_name='templates/geogebra_page.html')

            return render_template('geogebra_page.html', commands_text=commands_text, type='commands')


    return render_template("index.html", commands_text='')

@app.route('/parse_text', methods=('GET', 'POST'))
def parse_text():
    logger.info('Parsing text requested')

    if request.method == 'POST':
        text = str(request.form['text'])
        text = text.replace('\n', '')
        text = text.replace('\r', '\n')
        logger.info(text.find('\n'))
        logger.info(f'String to parse:{text}')

        if not text:
            flash('Commands are required!')

            return render_template("input.html", text=text)
        else:
            resp = text_analyze(text)

            # logger.info(f'Not formated lines: {objects}')

            # logger.info(f'Formated lines: {objects}')

            # parsed_text = '\n'.join(objects)
            parsed_text = resp.replace('\n', '')
            parsed_text = resp.replace('\r', '\n')
            logger.info('Result of parsing:')
            for line in parsed_text.split('\n'):
                logger.info(line)

            # logger.info(f'Result of parsing:\n{parsed_text}')

            return render_template("input.html", text=text, commands_text=parsed_text)

    return render_template("input.html", text='', commands_text='')

@app.route('/analysis_commands', methods=('GET', 'POST'))
def analyze_text():
    logger.info('Text commands analysis requested')
    if request.method == 'POST':
        commands_text = request.form['text_commands']
        text = request.form['text']
        screen_width = int(request.form['screen-width'])
        screen_height = int(request.form['screen-height'])
        logger.info(f'SCREEN SIZE: WIDTH: {screen_width}, HEIGHT: {screen_height}')
        # print(commands_text)
        logger.info(f'Text of commands:\n{text}')

        solving_template = 'templates/release_template.html'

        resp = text_splitter(commands_text, input_file_name=solving_template)
        # logger.info(task_parser.angles)
        # logger.info(task_parser.segments)
        # logger.info(task_parser.polygons)
        # logger.info(resp)
        # print(taskp.task_data)

        if resp == 200 and commands_text:

            return_dict = {}

            manager = multiprocessing.Manager()
            resp_dict = manager.dict()
            solving_process = multiprocessing.Process(target=get_dict_of_facts, args=(resp_dict, taskp.solver_data))
            solving_process.start()
            solving_process.join(SOLVING_TIME_LIMIT)


            solving_process.terminate()
            for key in resp_dict.keys():
                return_dict[key] = resp_dict[key]

            solving_process.is_alive()

            manager.shutdown()


            solving_finished = False

            try:
                task_parser.solver_data = return_dict['data']
                if return_dict['list of reason facts']['tree_levels']:
                    solving_finished = True

            except Exception as exc:
                logging.info(f'Error {exc}')

            facts = return_dict

            if solving_finished:
                logger.info('Question found')

                facts['list of reason facts'] = tree_levels_proccesing(facts['list of reason facts']['tree_levels'])
                fact_to_delete_duplicates = facts['list of reason facts']

                sorted_facts = [ii for n,ii in enumerate(fact_to_delete_duplicates) if ii not in fact_to_delete_duplicates[:n]]

                facts['list of reason facts'] = sorted_facts
                facts['question fact'] = sorted_facts[-1]

                solving_facts = facts['list of reason facts']

                answer_fact = facts['question fact']
                question_fact = taskp.task_data.questions[0]

                # for fact in [question_fact] + solving_facts:
                #     print(fact)
                #     print(fact_output(fact))
                #     print(type(fact.value))
                #     print(fact.value)

                logger.info('Text commands splitted and inserted in geogebra')

                # print(get_extreme_points(return_dict['data'].points))

                return render_template('geogebra_page.html',
                                       text=text,
                                       commands_text=commands_text,
                                       type='text',

                                       facts=solving_facts,

                                       question=question_fact,

                                       answer=answer_fact,

                                       necessary_coords_size = get_necessary_coords_size(return_dict['data'].points)
                                       )
            else:
                logger.info('Question not found')
                resp = text_splitter(commands_text, input_file_name='templates/drawing_template.html')

                if resp == 200 and commands_text:
                    logger.info('Text commands splitted and inserted in geogebra')
                    return render_template('geogebra_page.html', text=text, commands_text=commands_text, type='text')

        else:
            if not commands_text:
                flash('Commands are required!')
            else:
                flash(resp)
            return render_template('input.html', text=text, commands_text=commands_text, type='text')

    return render_template("input.html", commands_text='')

@app.route('/instruction_edit2508', methods=('GET', 'POST'))
def instruction():
    with open('templates/instruction.html', 'r') as file:
        text = file.read()

    logger.info('Instruction requested')

    if request.method == 'POST':
        logger.info('Instruction rewrite')
        text = request.form['instruction']
        with open('templates/instruction.html', 'w') as file:
            file.write(text)

    return render_template('instruction_input.html', text=text)

@app.route('/instruction', methods=['GET'])
def show_instruction():
    return render_template('instruction.html')

if __name__ == '__main__':
    app.run(debug=False, port=3600, threaded=False, host="0.0.0.0")