import math
import os

from cardan_grille import config
from cardan_grille.laquare import Laquare


class CardanGrille:
    MAX_LAQUARE_SIZE = config.encrypt_max_laquare() if config.encrypt_max_laquare() else 2048
    MIN_LAQUARE_SIZE = config.encrypt_min_laquare() if config.encrypt_min_laquare() else 256

    def __init__(self, i, o=None):
        self.input = i
        self.output = o
        self.is_file = os.path.exists(i)
        self.input_size = os.path.getsize(i) if self.is_file else len(i.encode())
        self.ls = self.get_latin_square()
        self.output_size = math.ceil(self.input_size / (self.ls.size ** 2)) * self.ls.size ** 2

    def decode(self):
        pass

    def encode(self):
        pass

    def get_latin_square(self):
        ls_size = math.ceil(self.input_size ** (1 / 2))
        if ls_size < self.MIN_LAQUARE_SIZE:
            ls_size = self.MIN_LAQUARE_SIZE
        elif ls_size > self.MAX_LAQUARE_SIZE:
            ls_size = self.MAX_LAQUARE_SIZE

        Laquare.process = self.process

        return Laquare(ls_size)

    @staticmethod
    def process(method, progress, cl='Laquare'):
        pass


if __name__ == '__main__':
    cg = CardanGrille('helló')
    print(cg.ls.size)
