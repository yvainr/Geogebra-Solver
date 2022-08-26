from flask import Flask, render_template, request, flash
import logging
import multiprocessing

from ggb_data_processing import task_parser as taskp
from ggb_html_generator.geogebra_html_generator import insert_commands
from ggb_drawer.polygon_drawer import text_splitter
from ggb_text_processing.language_interpreter import text_analyze
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

PYW_ROUTE = ''
# PYW_ROUTE = 'geogebra_app_release_version/Geogebra-Solver/web/' #comment if not pythonanywhere

SOLVING_TIME_LIMIT = 20 #seconds

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

    with open(PYW_ROUTE + 'static/quotes.txt', 'r') as fin:
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

            insert_commands(commands, input_file_name=f'{PYW_ROUTE}templates/drawing_template.html', output_file_name=f'{PYW_ROUTE}templates/geogebra_page.html')

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

        solving_template = f'{PYW_ROUTE}templates/release_template.html'

        # logger.info(task_parser.angles)
        # logger.info(task_parser.segments)
        # logger.info(task_parser.polygons)
        # logger.info(resp)
        # print(taskp.task_data)
        return_dict = {}

        try:
            return_dict = text_splitter(commands_text, input_file_name=solving_template)
            if type(return_dict) == str:
                logger.info(return_dict)
                return_dict = {'errors': [return_dict]}
            else:
                return_dict['errors'] = []

        except Exception as exc:
            logger.info(exc)
            logger.info('ERROR: Solver internal error')
            return_dict['errors'] = ['Solver internal error']

        # print(return_dict)

        if return_dict['errors'] == [] and commands_text:

            try:
                fact_key = list(return_dict['facts'].keys())[0]

                question_fact = fact_key
                solving_tree = return_dict['facts'][fact_key]['tree_levels']

            except Exception as exc:
                logger.info(f'ERROR: Question or fact tree not found\n{exc}')
                question_fact = None
                solving_tree = None
            # print(solving_tree)

            solving_finished = False

            try:
                if solving_tree:
                    solving_finished = True

            except Exception as exc:
                logging.info(f'ERROR: Error after solving: {exc}')

            if solving_finished and question_fact:
                logger.info('Question found')

                solving_tree = tree_levels_proccesing(solving_tree)
                fact_to_delete_duplicates = solving_tree

                sorted_facts = [ii for n,ii in enumerate(fact_to_delete_duplicates) if ii not in fact_to_delete_duplicates[:n]]

                solving_tree_list = sorted_facts

                answer_fact = solving_tree_list[-1]

                solving_facts = solving_tree_list
                # print(solving_facts)

                # for fact in [question_fact] + solving_facts:
                #     print(fact)
                #     print(fact_output(fact))
                #     print(type(fact.value))
                #     print(fact.value)

                logger.info('Text commands splitted and inserted in geogebra')

                return render_template('geogebra_page.html',
                                       text=text,
                                       commands_text=commands_text,
                                       type='text',

                                       facts=solving_facts,

                                       question=question_fact,

                                       answer=answer_fact,

                                       necessary_coords_size = get_necessary_coords_size(return_dict['data'].points) # TODO: можно заменить на taskp.solver_data.points
                                       )
            else:
                logger.info('Question not found')
                return_dict = text_splitter(commands_text, input_file_name=f'{PYW_ROUTE}templates/drawing_template.html')

                if type(return_dict) == str:
                    logger.info(return_dict)
                    return_dict = {'errors': [return_dict]}
                else:
                    return_dict['errors'] = []

                if return_dict['errors'] == [] and commands_text:
                    logger.info('Text commands splitted and inserted in geogebra')
                    return render_template('geogebra_page.html',
                                           text=text,
                                           commands_text=commands_text,
                                           type='text',

                                           necessary_coords_size = get_necessary_coords_size(return_dict['data'].points) # TODO: можно заменить на taskp.solver_data.points
                                           )
                else:
                    flash('\n'.join(return_dict['errors']))
                    return render_template('input.html', text=text, commands_text=commands_text, type='text')

        else:
            if not commands_text:
                flash('Commands are required!')
            else:
                flash('\n'.join(return_dict['errors']))
            return render_template('input.html', text=text, commands_text=commands_text, type='text')

    return render_template("input.html", commands_text='')


@app.route('/instruction_edit2508', methods=('GET', 'POST'))
def instruction():
    with open(f'{PYW_ROUTE}templates/instruction.html', 'r') as file:
        text = file.read()

    logger.info('Instruction requested')

    if request.method == 'POST':
        logger.info('Instruction rewrite')
        text = request.form['instruction']
        with open(f'{PYW_ROUTE}templates/instruction.html', 'w') as file:
            file.write(text)

    return render_template('instruction_input.html', text=text)


@app.route('/instruction', methods=['GET'])
def show_instruction():
    return render_template('instruction.html')


if __name__ == '__main__':
    app.run(debug=False, port=3600, threaded=False, host="0.0.0.0")