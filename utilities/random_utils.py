import random

from sql_utilites.sql_constants import INTEGER_INTERVAL


def gen_part(part_name, number_of_integer_rows):
    return part_name, *(random.randint(*INTEGER_INTERVAL) for _ in range(number_of_integer_rows))


def gen_ship(ship_name, available_weapons, available_hulls, available_engines):
    return ship_name, random.choice(available_weapons), random.choice(available_hulls), random.choice(available_engines)
