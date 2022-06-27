#Страница со списком функций
#https://wiki.geogebra.org/en/Point_Command

from geogebra_html_generator import insert_commands #импортируем библиотеку

task_file = open('example_commands.txt', 'r') #читаем файл с командами

commands_list = task_file.readlines() #разрезаем его на строки
commands_list = [command.replace('\n', '') for command in commands_list] #стираем в каждой строке \n

task_file.close() #закрываем файл

insert_commands(commands_list) #вставляем команды в html
