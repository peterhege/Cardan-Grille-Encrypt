import os

from cardan_grille.file_content import file_put_json_content, file_get_json_content

ROOT = os.path.realpath('{}/../'.format(os.path.dirname(os.path.realpath(__file__))))
CONFIG_FILE = '{root}/config.json'.format(root=ROOT)

if not os.path.exists(CONFIG_FILE):
    file_put_json_content(CONFIG_FILE, {})

CONFIG = file_get_json_content(CONFIG_FILE)

for key in ['x-rapidapi-key', 'api-max-size']:
    if key not in CONFIG:
        CONFIG[key] = None


def api_key(value=None):
    return val('x-rapidapi-key', value)


def api_max_size(value=None):
    return val('api-max-size', value)


def val(key, value=None):
    if value is not None:
        CONFIG[key] = value
    return CONFIG[key]


def save():
    file_put_json_content(CONFIG_FILE, CONFIG)
