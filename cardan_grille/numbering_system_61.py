import math


class NumberingSystem61:
    STOCK = list(map(str, range(0, 10))) \
            + list(map(chr, range(ord('a'), ord('z') + 1))) \
            + list(map(chr, range(ord('A'), ord('Y') + 1)))

    @staticmethod
    def from_dec(dec):
        buffer = []
        while True:
            divider = math.floor(dec / 61)
            mod = dec % 61
            buffer.insert(0, NumberingSystem61.STOCK[mod])
            dec = divider
            if not dec:
                break
        return ''.join(buffer)

    @staticmethod
    def to_dec(ns61):
        ns61 = ns61[::-1]
        dec = 0
        for exponent in range(len(ns61)):
            multiplier = NumberingSystem61.STOCK.index(ns61[exponent])
            dec += multiplier * (61 ** exponent)
        return dec


if __name__ == '__main__':
    print(NumberingSystem61.from_dec(10000))
    print(NumberingSystem61.to_dec('2FV'))
