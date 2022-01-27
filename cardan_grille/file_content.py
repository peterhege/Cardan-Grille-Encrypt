import json


def file_get_json_content(file):
    with open(file, 'r') as f:
        return json.load(f)


def file_put_json_content(file, content):
    with open(file, 'w') as f:
        json.dump(content, f)
