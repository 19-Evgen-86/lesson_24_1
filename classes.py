from dataclasses import dataclass


@dataclass
class Response:
    cmd1: str
    cmd2: str
    value1: str
    value2: str
    file_name: str


class MyExc(Exception):
    pass
