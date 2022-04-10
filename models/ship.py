from models.engine import Engine
from models.hull import Hull
from models.weapon import Weapon


class Ship:

    def __init__(self, ship_name, weapon_data, hull_data, engine_data):
        self.ship = ship_name
        self.weapon = Weapon(*weapon_data)
        self.hull = Hull(*hull_data)
        self.engine = Engine(*engine_data)

    def compare_ships_parts(self, part_name, obj):
        """
        Method that compares specific parts of ships
        :param part_name: name of required part
        :param obj: instance of ship object
        :return: difference between parts of ships models
        """
        part_diff = getattr(self, part_name).get_diff(getattr(obj, part_name))
        if part_diff:
            return f'{self.ship}, {getattr(self, part_name).primary_key}\n\t' + part_diff
        else:
            return ''
