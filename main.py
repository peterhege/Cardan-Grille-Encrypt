import json
import math
import os
import argparse

from cardan_grille.laquare import Laquare

CONFIG = {}

if not os.path.exists('config.json'):
    with open('config.json', 'w') as config:
        json.dump({}, config)

with open('config.json', 'r') as config:
    CONFIG = json.load(config)


def laquare_process(method, progress):
    print('Laquare.{method}: {progress}'.format(method=method, progress=progress))


def laquare_generate(args):
    size = args.size
    seed = args.seed if args.seed else None

    if args.max:
        Laquare.MAX_SIZE = args.max
    elif 'laquare-max-size' in CONFIG:
        Laquare.MAX_SIZE = CONFIG['laquare-max-size']

    ls = Laquare(size, seed)

    return ls


def set_config(args):
    if args.key:
        CONFIG['x-rapidapi-key'] = args.key
        print('x-rapidapi-key={}'.format(args.key))
    if args.max:
        CONFIG['laquare-max-size'] = args.max
        print('laquare-max-size={}'.format(args.max))

    with open('config.json', 'w') as config:
        json.dump(CONFIG, config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cardan Grille encryption')
    subparser = parser.add_subparsers(dest='command')

    encode = subparser.add_parser('encode')
    encode.add_argument('--input', '-i', type=str, help='input file or string', required=True)
    encode.add_argument('--output', '-o', type=str, help='output file')

    decode = subparser.add_parser('decode')
    decode.add_argument('--input', '-i', type=str, help='input file or string', required=True)
    decode.add_argument('--output', '-o', type=str, help='output file')

    ls = subparser.add_parser('laquare')
    ls.add_argument('--size', '-s', type=int, help='Latin Square size', required=True)
    ls.add_argument('--seed', type=int, help='Latin Square random seed')
    ls.add_argument('--max', '-m', type=int, help='Max size of a Latin Square by Laquare API')
    ls.add_argument('--pretty', action='store_true', help='Show result in table')

    config = subparser.add_parser('config')
    config.add_argument('--key', '-k', type=str, help='x-rapidapi-key: https://rapidapi.com/peterhege/api/laquare')
    config.add_argument('--max', '-m', type=int, help='Max size of a Latin Square by Laquare API')

    args = parser.parse_args()

    if args.command == 'config':
        set_config(args)
        exit()

    if 'x-rapidapi-key' not in CONFIG:
        print('RapidApi key not found. Use this command: py main.py config --key=[Your RapidApi key]')

    Laquare.X_RAPIDAPI_KEY = CONFIG['x-rapidapi-key']
    Laquare.process = laquare_process

    if not Laquare.api_key_is_valid():
        print('Invalid RapidApi Key: {}'.format(Laquare.X_RAPIDAPI_KEY))

    if args.command == 'laquare':
        ls = laquare_generate(args)
        if args.pretty:
            ls.print()
        else:
            print(ls.ls)
        exit()

    Laquare.X_RAPIDAPI_KEY = args.key

    if args.mode == 'e':
        # File Size
        c = os.path.getsize(args.input)

        # Latin Square Size By Content
        n = math.ceil(c ** (1 / 2))
        n = n if n > 10 else 10

        # Generate Latin Square
        Laquare.process = laquare_process
        ls = Laquare(n)

        # Fix size
        n = ls.size

        # Fill content
        c_max = math.ceil(c / (n ** 2)) * n ** 2
        buffer = [[0 for i in range(n)] for j in range(n)]
