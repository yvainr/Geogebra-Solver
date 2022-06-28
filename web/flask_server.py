from flask import Flask, render_template, request, url_for, flash, redirect
from time import sleep
from werkzeug.exceptions import abort
import logging
import sqlite3
from drawer_ggb.geogebra_html_generator import insert_commands

app = Flask(__name__, template_folder='./templates',static_folder='./static')
app.config['SECRET_KEY'] = ''
app.config['TEMPLATES_AUTO_RELOAD'] = True


def split_commands(commands_text: str):
    commands_list = commands_text.split('\n')  # разрезаем его на строки
    commands_list = [command.replace('\n', '').replace('\r', '') for command in commands_list]  # стираем в каждой строке \n
    commands_list = [command for command in commands_list if command]
    return commands_list

@app.route('/', methods=('GET', 'POST'))
def index(commands_text=''):
    # if request.method == 'POST':
    commands_text = request.args.get('commands_text')
    # print(repr(commands_text))
    return render_template('index.html', commands_text=commands_text)

@app.route('/render_geogebra', methods=('GET', 'POST'))
def create():

    if request.method == 'POST':
        commands_text = request.form['commands']

        if not commands_text:
            flash('Commands are required!')

        commands = split_commands(commands_text)
        print(commands)
        insert_commands(commands, input_file_name='web/templates/template.html', output_file_name='web/templates/geogebra_page.html')

        return render_template('geogebra_page.html', commands_text=commands_text)

    return render_template("index.html", commands_text='')

if __name__ == '__main__':
    app.run(debug=False, port=5000, threaded=False)