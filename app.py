import os
import re

import marshmallow_dataclass
from flask import Flask, request

from classes import Response, MyExc

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


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
            return [line for line in obj if re.search(value, line) is not None]
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

        responseShema: marshmallow_dataclass = marshmallow_dataclass.class_schema(Response)
        response: Response = responseShema().load(request.json)
        # получаем дескриптор файла
        file: str = get_file(response.file_name)
        # создаем генератор для чтения файла
        lines = (line for line in open(file))

        result_cmd1 = use_command(response.cmd1, response.value1, lines)
        result_cmd2 = use_command(response.cmd2, response.value2, result_cmd1)
        result = '\n'.join(result_cmd2)
        print(result)
        return app.response_class(result, content_type="text/plain"), 200

    except MyExc as e:

        return app.response_class(str(e), content_type="text/plain"), 400


if __name__ == '__main__':
    app.run(debug=True)
