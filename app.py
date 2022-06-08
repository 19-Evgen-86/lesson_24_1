import os
import re

from flask import Flask, request
from classes import Response, MyExc
import marshmallow_dataclass

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

LST_PARAM = ['cmd1', 'cmd2', 'file_name']
LST_CMD = ['filter', 'map', 'unique', 'sort', 'limit']


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
        case 'regex':
            return list(map(lambda line: re.findall(value, line), obj))
        case 'file_name':
            pass
        case _:
            raise MyExc("no command")


def get_file(file_name):
    file = os.path.join(DATA_DIR, file_name)
    if os.path.exists(file):
        return file
    else:
        raise MyExc("File not Found")


@app.route("/perform_query", methods=["POST"])
def perform_query():
    try:

        responseShema = marshmallow_dataclass.class_schema(Response)
        response = responseShema().load(request.json)
        # получаем дескриптор файла
        file = get_file(response.file_name)
        # создаем генератор для чтения файла
        lines = (line for line in open(file))

        for cmd, value in response.__dict__.items():
            lines = use_command(cmd, value, lines)
        result = '\n'.join(lines)

        return app.response_class(result, content_type="text/plain"), 200

    except MyExc as e:

        return app.response_class(str(e), content_type="text/plain"), 400


if __name__ == '__main__':
    app.run(debug=True)
