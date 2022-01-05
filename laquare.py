import json
import math
import os
import random

import requests


class Laquare:
    SQUARES_PATH = 'squares'
    X_RAPIDAPI_KEY = ''
    MAX_SIZE = 256

    def __init__(self, size, state=None):
        self.ls = None
        self.base = None
        self.size = size
        self.state = state if state else random.randint(0, 256000)
        self.x = self.state

        self.slices = math.ceil(self.size / Laquare.MAX_SIZE)
        self.n = math.ceil(self.size / self.slices)
        self.size = self.slices * self.n

        self.file_name = '{path}/{size}_{state}.json'.format(size=self.size, state=self.state, path=self.SQUARES_PATH)
        if os.path.exists(self.file_name):
            self.from_file()
        else:
            self.from_api()

    def from_file(self):
        Laquare.process('from_file', self.file_name)
        with open(self.file_name) as json_file:
            self.ls = json.load(json_file)

    def from_api(self):
        self.ls = [[-1 for i in range(self.size)] for j in range(self.size)]
        self.create_base()
        self.create_slices()

        if not os.path.isdir(Laquare.SQUARES_PATH):
            os.mkdir(Laquare.SQUARES_PATH)

        with open(self.file_name, 'w') as out_file:
            json.dump(self.ls, out_file)

    def create_base(self):
        Laquare.process('create_base', 0)
        self.base = self.generate(self.slices, self.state)
        Laquare.process('create_base', 100)

    def create_slices(self):
        Laquare.process('create_slices', 0)

        for i in range(self.slices):
            for j in range(self.slices):
                Laquare.process('create_slices', (i * self.slices + j + 1) * 100 / (self.slices * self.slices))
                self.create_slice(i, j)

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

    def generate(self, size, state):
        Laquare.process('generate', [size, state])
        response = Laquare.api_call('GET', 'generate', {"size": size, "state": state})

        if not response.ok:
            raise Exception(response.status_code, response.text)

        return json.loads(response.text)['data']

    def print(self):
        for row in self.ls:
            print()
            for n in row:
                print(n, end='\t')

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
    print(l.state)
