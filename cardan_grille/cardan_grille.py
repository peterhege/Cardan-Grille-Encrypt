import math
import os
import random
import re
import time

from cardan_grille import config
from cardan_grille.laquare import Laquare
from cardan_grille.numbering_system_61 import NumberingSystem61


class CardanGrille:
    MAX_LAQUARE_SIZE = config.encrypt_max_laquare() if config.encrypt_max_laquare() else 2048
    MIN_LAQUARE_SIZE = config.encrypt_min_laquare() if config.encrypt_min_laquare() else 256

    def __init__(self, i, o=None):
        self.t = time.time()
        self.input = i
        self.output = o
        self.is_file = os.path.exists(i)
        self.input_size = os.path.getsize(i) if self.is_file else len(i.encode())
        self.symbol = -1
        self.row = -1
        self.column = -1
        self.trim_from = b'%cardan_grille_decode_trim_from%'
        self.buffer = None
        self.ls = None
        self.append = None
        if self.output is not None:
            with open(self.output, 'w') as file:
                file.write('')

    def create_append(self):
        output_size = math.ceil(self.input_size / (self.ls.size ** 2)) * self.ls.size ** 2
        CardanGrille.process('create_append', 0)
        append_bytes = output_size - self.input_size
        self.input_size += append_bytes
        self.append = self.trim_from
        if len(self.trim_from) <= append_bytes:
            append_bytes = append_bytes - len(self.trim_from)
        else:
            append_bytes = self.ls.size ** 2 - (len(self.trim_from) - append_bytes)
            self.input_size += self.ls.size ** 2
        for i in range(append_bytes):
            self.append += chr(random.randint(0, 127)).encode()
            CardanGrille.process('create_append', (i + 1) * 100 / append_bytes)

    def decode(self, key):
        CardanGrille.process('decode', 0)
        (size, ls_max, api_max, seed) = tuple(map(NumberingSystem61.to_dec, key.split('Z')))
        Laquare.MAX_SIZE = ls_max
        Laquare.API_MAX_SIZE = api_max
        self.ls = self.get_latin_square(seed, size)
        self.run(self.decode_byte)

    def encode(self, seed):
        CardanGrille.process('encode', 0)
        self.ls = self.get_latin_square(seed)
        self.create_append()
        self.run(self.encode_byte)
        print('Key:', '{size}Z{max}Z{api_max}Z{seed}'.format(
            size=NumberingSystem61.from_dec(self.ls.size),
            max=NumberingSystem61.from_dec(Laquare.MAX_SIZE),
            api_max=NumberingSystem61.from_dec(Laquare.API_MAX_SIZE),
            seed=NumberingSystem61.from_dec(self.ls.seed)
        ))

    def decode_byte(self, i):
        if (i % self.ls.size) == 0:
            self.column = (self.column + 1) % self.ls.size
        self.symbol = (self.symbol + 1) % self.ls.size
        self.row = self.ls.ls[self.column][self.symbol]
        CardanGrille.process('decode', (i + 1) * 100 / self.input_size)

    def encode_byte(self, i):
        if (i % self.ls.size) == 0:
            self.symbol = (self.symbol + 1) % self.ls.size

        self.row = (self.row + 1) % self.ls.size
        self.column = self.ls.ls[self.row].index(self.symbol)
        CardanGrille.process('encode', (i + 1) * 100 / self.input_size)

    def store(self, one_byte, i, callback):
        if (i % self.ls.size ** 2) == 0:
            self.save()
            self.buffer = [[b'' for k in range(self.ls.size)] for j in
                           range(self.ls.size)]
        callback(i)
        self.buffer[self.row][self.column] = one_byte

    def save(self, last=False):
        if self.buffer is None:
            return
        if self.output is None:
            self.output = []
        r = b''.join([b''.join(row) for row in self.buffer])
        if last:
            r = re.sub(self.trim_from + b'.*', b'', r, flags=re.S)
        if type(self.output) is list:
            self.output.append(r)
        else:
            mode = 'ab' if os.path.exists(self.output) else 'wb'
            with open(self.output, mode) as o:
                o.write(r)

    def run(self, callback):
        if self.is_file:
            with open(self.input, "rb") as in_file:
                part_size = 1024 ** 2
                part = in_file.read(part_size)
                i = 0
                while part:
                    for j in range(len(part)):
                        one_byte = bytes(part[j:j + 1])
                        self.store(one_byte, i + j, callback)
                    (part, i) = (in_file.read(part_size), i + j + 1)
        else:
            b = self.input.encode()
            for i in range(len(b)):
                one_byte = bytes(b[i:i + 1])
                self.store(one_byte, i, callback)

        if self.append:
            for j in range(len(self.append)):
                one_byte = bytes(self.append[j:j + 1])
                self.store(one_byte, i + j, callback)

        self.save(True)

        CardanGrille.process('runtime', time.time() - self.t)

        if type(self.output) is list:
            try:
                print(b''.join(self.output).decode())
            except:
                print(b''.join(self.output))

    def get_latin_square(self, seed, ls_size=None):
        CardanGrille.process('get_latin_square', 0)

        if ls_size is None:
            ls_size = math.ceil(self.input_size ** (1 / 2))
            if ls_size < self.MIN_LAQUARE_SIZE:
                ls_size = self.MIN_LAQUARE_SIZE
            elif ls_size > self.MAX_LAQUARE_SIZE:
                ls_size = self.MAX_LAQUARE_SIZE

        ls = Laquare(ls_size, seed)
        CardanGrille.process('get_latin_square', 100)
        return ls

    @staticmethod
    def process(method, progress):
        pass


if __name__ == '__main__':
    cg = CardanGrille('helló')
    print(cg.ls.size)
