import logging


def insert_commands(list_of_commands: list, output_file_name='page_test.html'):
    """Принимает на вход список строк-команд geogebra, возвращает код html страницы, 
    отображающей чертёж, постороенный по этим командам и создаёт такой файл в той же дирректории, что и запущена"""

    js_commands_text = ''

    for command in list_of_commands:
        js_commands_text += '    ' * 3 + f'ggbApplet.evalCommand(\'{command}\'); \n'

    html_page_file = open('template.html', 'r')

    html_code = html_page_file.read()

    html_page_file.close()

    edited_code = html_code.replace('//////',
                                    js_commands_text)  # пока что так, но потом нужно будет перейти на шаблоны jinja2

    output_html = open('page_test.html', 'w')

    output_html.write(edited_code)

    output_html.close()

    return edited_code
