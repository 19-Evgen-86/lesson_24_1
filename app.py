import os

from flask import Flask, request

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

LST_PARAM = ['cmd1', 'cmd2', 'value1', 'value2', 'file_name']
LST_CMD = ['filter', 'map', 'unique', 'sort', 'limit']


def get_param(args):
    """
    проверяем наличие параметров в запросе. если все есть, то возвращаем словарь
    :param args:
    :return:
    """
    check_param = lambda lst_param, args: [param for param in lst_param if param not in args.keys()]
    no_param = check_param(LST_PARAM, args)
    if not no_param:
        return {key: value for key, value in args.items()}
    else:
        return f" отсутствуют параметры {no_param}", 400


def check_file(file_name):
    file = os.path.join(DATA_DIR, file_name)
    return file if os.path.exists(file) else "nonfiole"


def use_command(cmd, value, obj):
    match cmd:
        case 'filter':
            res = filter(lambda line: line == value, obj)
        case "map":
            res = list(map(lambda line: line.split(), obj))[int(value)]
        case 'unique':
            res = set(obj)
        case 'sort':
            revers = value == "desc"
            res = sorted(obj, reverse=revers)
        case 'limit':
            res = 1

@app.route("/perform_query", methods=["GET"])
def perform_query():
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат
    try:
        param = get_param(request.args)
        file = check_file(param["file_name"])
        lines = (line for line in open(param["file_name"]))
        print(lines)

    except:
        pass

    return app.response_class('', content_type="text/plain")


if __name__ == '__main__':
    app.run()
