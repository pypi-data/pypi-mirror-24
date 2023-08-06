import math
import random
import sys


# generate a guassrandom
def guassrandom():
    u = random.random()
    v = random.random()
    w = math.sin(2 * math.pi * v) * pow(((-2) * math.log10(u)), 1 / 2)
    return w


def print_lol(the_list, indent=False, level=0, fn=sys.stdout):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level + 1, fn)
        else:
            if indent:
                print('|', end='')
                for tab_stop in range(level):
                    print('-' * 4, end='', file=fn)
            print(each_item, file=fn)
