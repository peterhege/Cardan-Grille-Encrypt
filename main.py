import math
import os
import argparse

from laquare import Laquare


def h(msg):
    parser.print_usage()
    print()
    print(msg)
    exit()


def process(method, progress):
    print('Laquare.{method}: {progress}'.format(method=method, progress=progress))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cardan Grille encryption')
    parser.add_argument('--mode', '-m', type=str, help='d: decode | e: encode', required=True)
    parser.add_argument('--input', '-i', type=str, help='input file', required=True)
    parser.add_argument('--output', '-o', type=str, help='output file', required=True)
    parser.add_argument('--key', '-k', type=str, help='x-rapidapi-key: https://rapidapi.com/peterhege/api/laquare',
                        required=True)

    args = parser.parse_args()

    Laquare.X_RAPIDAPI_KEY = args.key

    if args.mode not in ['d', 'e']:
        h('Possible values for MODE: d or e')

    if not os.path.exists(args.input):
        h("'{}' file not exist".format(args.input))

    if not Laquare.api_key_is_valid():
        h("'{}' not subscribed to this API.".format(args.key))

    if args.mode == 'e':
        # File Size
        c = os.path.getsize(args.input)

        # Latin Square Size By Content
        n = math.ceil(c ** (1 / 2))
        n = n if n > 10 else 10

        # Generate Latin Square
        Laquare.process = process
        ls = Laquare(n)

        # Fix size
        n = ls.size

        # Fill content
        c_max = math.ceil(c / (n ** 2)) * n ** 2
        buffer = [[0 for i in range(n)] for j in range(n)]
