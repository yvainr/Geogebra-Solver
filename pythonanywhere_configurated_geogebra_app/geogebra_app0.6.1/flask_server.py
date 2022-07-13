from flask import Flask, render_template, request, url_for, flash, redirect
from time import sleep
from werkzeug.exceptions import abort
import logging
import sqlite3
from geogebra_html_generator import insert_commands
import triangle_drawer
import task_parser as taskp
from polygon_drawer import text_splitter
from language_interpreter import main_func as text_analyze

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO

)

logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='./templates',static_folder='./static')
app.config['SECRET_KEY'] = ''
app.config['TEMPLATES_AUTO_RELOAD'] = True

# def text_splitter(text):
#     text = text.split('\n')
#
#     try:
#         taskp.polygons_create(text[1])
#         taskp.segments_create(text[2])
#         taskp.angles_create(text[3])
#         taskp.segments_relations_create(text[4])
#         taskp.angles_relations_create(text[5])
#         taskp.line_intersection_create(text[6])
#     except IndexError:
#         pass
#
#     triangle_from_task_drawer(taskp.polygons[0].points[0].name, taskp.polygons[0].points[1].name, taskp.polygons[0].points[2].name)


def split_commands(commands_text: str):
    commands_list = commands_text.split('\n')  # разрезаем его на строки
    commands_list = [command.replace('\n', '').replace('\r', '') for command in commands_list]  # стираем в каждой строке \n
    commands_list = [command for command in commands_list if command]
    return commands_list

@app.route('/', methods=('GET', 'POST'))
def index(commands_text=''):
    logger.info('Commands input page requested')
    # if request.method == 'POST':
    commands_text = request.args.get('commands_text')
    logger.info(f'Commands: {commands_text}')
    # print(repr(commands_text))
    return render_template('index.html', commands_text=commands_text)

@app.route('/text_input', methods=('GET', 'POST'))
def text_input(text='', commands_text=''):
    logger.info('Text input page requested')
    # if request.method == 'POST':
    text = request.args.get('text')
    commands_text = request.args.get('commands_text')

    logger.info(f'Text:{text}')
    logger.info(f'Text commads:\n{commands_text}')

    # print(repr(commands_text))
    return render_template('input.html', text=text, commands_text=commands_text)

@app.route('/render_geogebra', methods=('GET', 'POST'))
def create():
    logger.info('Render page requested')
    if request.method == 'POST':
        commands_text = request.form['commands']

        if not commands_text:
            flash('Commands are required!')

        commands = split_commands(commands_text)

        logger.info(f'Recieved geogebra commands: {commands}')

        insert_commands(commands, input_file_name='geogebra_app/templates/template.html', output_file_name='geogebra_app/templates/geogebra_page.html')

        return render_template('geogebra_page.html', commands_text=commands_text, type='commands')

    return render_template("index.html", commands_text='')

@app.route('/parse_text', methods=('GET', 'POST'))
def parse_text():
    logger.info('Parsing text requested')

    if request.method == 'POST':
        text = request.form['text']
        logger.info(f'String to parse:{text}')

        objects = text_analyze(text) #array of lists of objects
        logger.info(objects)
        parsed_text = ''
        for object_class in objects:
            parsed_text += (', '.join(object_class) + '\n')



        logger.info(f'Result of parsing:\n{parsed_text}')

        return render_template("input.html", text=text, commands_text=parsed_text)

    return render_template("input.html", text='', commands_text='')

@app.route('/analysis_commands', methods=('GET', 'POST'))
def analyze_text():
    logger.info('Text commands analysis requested')
    if request.method == 'POST':
        commands_text = request.form['text_commands']
        text = request.form['text']
        # print(commands_text)


        text_splitter(commands_text)

        logger.info('Text commands splitted and inserted in geogebra')
        # if not commands_text:
        #     flash('Commands are required!')
        #
        # commands = split_commands(commands_text)
        # print(commands)
        # insert_commands(commands, input_file_name='web/templates/template.html', output_file_name='web/templates/geogebra_page.html')
        #
        return render_template('geogebra_page.html', text=text, commands_text=commands_text, type='text')

    return render_template("input.html", commands_text='')

if __name__ == '__main__':
    app.run(debug=False, port=5000, threaded=False)