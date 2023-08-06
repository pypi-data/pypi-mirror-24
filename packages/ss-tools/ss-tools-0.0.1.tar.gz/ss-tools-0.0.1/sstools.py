import math
import random


# generate a guassrandom
def guassrandom():
    u = random.random()
    v = random.random()
    w = math.sin(2 * math.pi * v) * pow(((-2) * math.log10(u)), 1 / 2)
    return w


def print_lol(the_list):
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item)
        else:
            print(each_item)
