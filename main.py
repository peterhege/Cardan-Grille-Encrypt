import os
import argparse
import sys

from cardan_grille.cardan_grille import CardanGrille
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
        print('Laquare.{method}(): {progress:.4f}%'.format(method=method, progress=progress), end='\r')
        if progress == 100:
            print()


def cardan_grille_process(method, progress):
    if method == 'runtime':
        print('CardanGrille runtime: {:.2f}s'.format(progress))
    else:
        print('CardanGrille.{method}(): {progress:.4f}%'.format(method=method, progress=progress), end='\r')
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
    if args.cgmax:
        print('encrypt-max-laquare={}'.format(config.encrypt_max_laquare(args.cgmax)))
    if args.cgmin:
        print('encrypt-min-laquare={}'.format(config.encrypt_min_laquare(args.cgmin)))

    config.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Cardan Grille encryption')
    subparser = parser.add_subparsers(dest='command')

    for cmd in ['encode', 'decode']:
        cmd_parser = subparser.add_parser(cmd, help='{} a file or input string'.format(cmd))
        cmd_parser.add_argument('--input', '-i', type=str, help='input file or string', required=True)
        cmd_parser.add_argument('--output', '-o', type=str, help='output file')
        cmd_parser.add_argument('--progress', action='store_true', help='Show generating progress')
        if cmd == 'decode':
            cmd_parser.add_argument('--key', type=str, help='Decode key', required=True)
        else:
            cmd_parser.add_argument('--seed', type=int, help='Seed for random')

    ls = subparser.add_parser('laquare', help='Generate a Latin Square')
    ls.add_argument('--size', '-s', type=int, help='Latin Square size', required=True)
    ls.add_argument('--seed', type=int, help='Latin Square random seed')
    ls.add_argument('--max', '-m', type=int, help='Max size of a Latin Square by Laquare API')
    ls.add_argument('--print', help='Show result in table', choices=['table', 'list'])
    ls.add_argument('--progress', action='store_true', help='Show generating progress')
    ls.add_argument('--regenerate', action='store_true', help='Print command for regenerate')

    conf = subparser.add_parser('config', help='Set config')
    conf.add_argument('--key', '-k', type=str, help='x-rapidapi-key: https://rapidapi.com/peterhege/api/laquare')
    conf.add_argument('--apimax', type=int, help='Max size of a Latin Square by Laquare API')
    conf.add_argument('--cgmax', type=int, help='Max Latin Square size for Encrypt')
    conf.add_argument('--cgmin', type=int, help='Min Latin Square size for Encrypt')

    clear = subparser.add_parser('clear', help='Remove all cache file')

    args = parser.parse_args()

    if args.command == 'config':
        set_config(args)
        exit()

    if args.command == 'laquare':
        laquare_generate(args)
        exit()

    if args.command == 'encode' or args.command == 'decode':
        if args.progress:
            Laquare.process = laquare_process
            CardanGrille.process = cardan_grille_process

        out = args.output if args.output else None
        if out and os.path.exists(out):
            continues = ''
            while continues.lower() not in ['y', 'n', 'yes', 'no']:
                continues = input('{} out file already exist. Continues? [y,n]: '.format(out))
            if continues.lower() not in ['y', 'yes']:
                exit()

        if args.command == 'encode':
            seed = args.seed if args.seed else None
        else:
            seed = None

        cg = CardanGrille(args.input, out)
        getattr(cg, args.command)(seed if args.command == 'encode' else args.key)
        exit()

    if args.command == 'clear':
        files = os.listdir(Laquare.SQUARES_PATH)
        for filename in files:
            os.remove('{}/{}'.format(Laquare.SQUARES_PATH, filename))
        print('{} file removed from {}'.format(len(files), Laquare.SQUARES_PATH))
