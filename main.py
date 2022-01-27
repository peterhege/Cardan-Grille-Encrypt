import math
import os
import argparse
import sys

from cardan_grille.laquare import Laquare
from cardan_grille import config


def laquare_process(method, progress):
    if method == 'generate':
        # print('Laquare.generate(size={}, seed={})'.format(progress[0], progress[1]))
        return
    elif method == 'from_file':
        print('Laquare.from_file(): {file}'.format(file=progress))
    elif method == 'runtime':
        print('Laquare runtime: {:.2f}s'.format(progress))
    else:
        print('Laquare.{method}(): {progress:.2f}%'.format(method=method, progress=progress), end='\r')
        if progress == 100:
            print()


def laquare_generate(args):
    size = args.size
    seed = args.seed if args.seed else None

    if args.max:
        Laquare.MAX_SIZE = args.max

    if args.progress:
        Laquare.process = laquare_process

    if not Laquare.X_RAPIDAPI_KEY:
        print('RapidApi key not found for https://rapidapi.com/peterhege/api/laquare.')
        print('Use this command: py main.py config --key=[Your RapidApi key]')
        exit()

    if not Laquare.api_key_is_valid():
        print('Invalid RapidApi Key for https://rapidapi.com/peterhege/api/laquare:')
        print(Laquare.X_RAPIDAPI_KEY)
        print('Use this command: py main.py config --key=[Your Valid RapidApi key]')
        exit()

    ls = Laquare(size, seed)

    if args.print:
        if args.print == 'table':
            ls.print()
        else:
            print(ls.ls)

    if args.regenerate:
        print('py {file} laquare --size={size} --seed={seed} --max={max}'.format(
            file=sys.argv[0],
            size=ls.size,
            seed=ls.seed,
            max=ls.MAX_SIZE
        ))


def set_config(args):
    if args.key:
        print('x-rapidapi-key={}'.format(config.api_key(args.key)))
    if args.apimax:
        print('api-max-size={}'.format(config.api_max_size(args.apimax)))

    config.save()


def decode(args):
    pass


def encode(args):
    pass


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
    ls.add_argument('--print', help='Show result in table', choices=['table', 'list'])
    ls.add_argument('--progress', action='store_true', help='Show generating progress')
    ls.add_argument('--regenerate', action='store_true', help='Print command for regenerate')

    conf = subparser.add_parser('config')
    conf.add_argument('--key', '-k', type=str, help='x-rapidapi-key: https://rapidapi.com/peterhege/api/laquare')
    conf.add_argument('--apimax', '-m', type=int, help='Max size of a Latin Square by Laquare API')

    args = parser.parse_args()

    if args.command == 'config':
        set_config(args)
        exit()

    if args.command == 'laquare':
        laquare_generate(args)
        exit()

    Laquare.process = laquare_process

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
