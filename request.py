import requests
import json

url = "http://127.0.0.1:5000/perform_query"

payload = {
    'file_name': 'apache_logs.txt',
    'cmd1': 'regex',
    'value1': r'images/\\w+\\.png',
    'cmd2': 'sort',
    'value2': 'asc'
}

headers = {'Content-Type': 'application/json'}
requests.request("POST", url, data=json.dumps(payload), headers=headers)
