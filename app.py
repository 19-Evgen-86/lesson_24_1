import os

from flask import Flask, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

LST_PARAM = ['cmd1', 'cmd2', 'file_name']
LST_CMD = ['filter', 'map', 'unique', 'sort', 'limit']


def check_file(file_name):
    file = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file):
        return file
    else:
        raise MyExc("no File")


class MyExc(Exception):
    pass


def use_command(cmd, value, obj):
    match cmd:
        case 'filter':
            return list(filter(lambda line: value in line, obj))
        case "map":
            return list(map(lambda line: line.split()[int(value)], obj))
        case 'unique':
            return set(obj)
        case 'sort':
            revers = value == "desc"
            return list(sorted(obj, reverse=revers))
        case 'limit':
            return list(obj[:int(value)])
        case _:
            raise MyExc("no command")


def get_file_name(agrs):
    file_name = agrs.get("file_name")
    if file_name:
        return check_file(file_name)
    else:
        raise MyExc("file not found")


def get_param(args):
    permitted_command = ['filter', 'map', 'unique', 'sort', 'limit']
    commands = {key: value for key, value in request.args.items()}
    del commands['file_name']
    no_cmd = [cmd for cmd in permitted_command if cmd not in cmd]
    if no_cmd:
        raise MyExc(f'{no_cmd} не известные команды')
    else:
        return commands


@app.route("/perform_query", methods=["GET"])
def perform_query():
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат
    try:
        # получаем дескриптор файла
        file = get_file_name(request.args)
        # получаем словарь с командами
        commands = get_param(request.args)
        # создаем генератор для чтения файла
        lines = (line for line in open(file))

        for cmd, value in commands.items():
            lines = use_command(cmd, value, lines)

        result = '\n'.join(lines)

        return app.response_class(result, content_type="text/plain"), 200

    except MyExc as e:

        return app.response_class(str(e), content_type="text/plain"), 400


if __name__ == '__main__':
    app.run(DEBUG=True)
