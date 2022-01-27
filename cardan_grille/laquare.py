import json
import math
import os
import random
import time

import requests
import hashlib

from cardan_grille import config
from cardan_grille.file_content import file_get_json_content, file_put_json_content


class Laquare:
    SQUARES_PATH = '{root}/squares'.format(root=config.ROOT)
    X_RAPIDAPI_KEY = config.api_key()
    MAX_SIZE = config.api_max_size() if config.api_max_size() else 256
    API_MAX_SIZE = 1024

    def __init__(self, size, seed=None):
        t = time.time()
        self.ls = None
        self.base = None
        self.size = size
        self.seed = seed if seed else random.randint(0, 256000)
        self.x = self.seed

        self.slices = math.ceil(self.size / Laquare.MAX_SIZE)
        self.n = math.ceil(self.size / self.slices)
        self.size = self.slices * self.n

        h = hashlib.md5('{size}|{max}|{seed}'.format(max=self.MAX_SIZE, size=self.size, seed=self.seed).encode())
        self.file_name = os.path.realpath('{path}/{hash}.json'.format(path=self.SQUARES_PATH, hash=h.hexdigest()))

        if self.MAX_SIZE > self.API_MAX_SIZE:
            self.MAX_SIZE = self.API_MAX_SIZE

        if os.path.exists(self.file_name):
            self.from_file()
        else:
            self.from_api()

        Laquare.process('runtime', time.time() - t)

    def from_file(self):
        Laquare.process('from_file', self.file_name)
        self.ls = file_get_json_content(self.file_name)

    def from_api(self):
        self.ls = [[-1 for i in range(self.size)] for j in range(self.size)]
        self.create_base()
        self.create_slices()

        if not os.path.isdir(Laquare.SQUARES_PATH):
            os.mkdir(Laquare.SQUARES_PATH)

        file_put_json_content(self.file_name, self.ls)

    def create_base(self):
        Laquare.process('create_base', 0)
        self.base = self.generate(self.slices, self.seed)
        Laquare.process('create_base', 100)

    def create_slices(self):
        Laquare.process('create_slices', 0)

        for i in range(self.slices):
            for j in range(self.slices):
                self.create_slice(i, j)
                Laquare.process('create_slices', (i * self.slices + j + 1) * 100 / (self.slices * self.slices))

    def create_slice(self, i, j):
        increase = self.base[i][j] * self.n
        (x, y) = (i * self.n, j * self.n)
        ls = self.generate(self.n, self.lcg())
        for i in range(self.n):
            for j in range(self.n):
                self.ls[x + i][y + j] = ls[i][j] + increase

    def lcg(self):
        self.x = int((1664525 * self.x + 1013904223) % math.pow(2, 32))
        return self.x

    def generate(self, size, seed):
        Laquare.process('generate', [size, seed])
        if size == 1:
            return [[0]]
        elif size == 2:
            r = seed % 2
            return [[r, int(not r)], [int(not r), r]]

        response = Laquare.api_call('GET', 'generate', {"size": size, "state": seed})

        if not response.ok:
            raise Exception(response.status_code, response.text)

        return json.loads(response.text)['data']

    def print(self):
        for row in self.ls:
            for n in row:
                print('| {0:>{1}}'.format(n, len(str(self.size - 1))), end=' ')
            print('|')

    @staticmethod
    def api_call(method, endpoint, querystring=None):
        url = f"https://laquare.p.rapidapi.com/{endpoint}".format(endpoint=endpoint)

        headers = {
            'x-rapidapi-host': "laquare.p.rapidapi.com",
            'x-rapidapi-key': Laquare.X_RAPIDAPI_KEY
        }

        if querystring is None:
            querystring = {}

        return requests.request(method, url, headers=headers, params=querystring)

    @staticmethod
    def api_key_is_valid():
        return Laquare.api_call('GET', 'generate', {"size": 1}).ok

    @staticmethod
    def process(method, progress):
        pass


def process(method, progress):
    print('Laquare.{method}: {progress}'.format(method=method, progress=progress))


if __name__ == '__main__':
    Laquare.process = process
    Laquare.MAX_SIZE = 4
    print('API Key:', end='')
    Laquare.X_RAPIDAPI_KEY = input()
    l = Laquare(5, 101)
    print(l.seed)
