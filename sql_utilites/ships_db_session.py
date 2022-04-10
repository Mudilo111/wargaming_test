from sql_utilites.base_sql_session import BaseSQLSession
from sql_utilites.sql_queries import *
from sql_utilites.sql_constants import *
from utilities.random_utils import gen_part, gen_ship
from tets_data.constants import *
from models.ship import Ship
from models.weapon import Weapon
from models.engine import Engine
from models.hull import Hull

import random


class ShipsDBSession(BaseSQLSession):

    def create_tables(self):
        """
        Method that creates required tables (weapons, engines, hulls, Ships)
        :return: None
        """
        self.execute_query(CREATE_TABLE_WEAPONS)
        self.execute_query(CREATE_TABLE_ENGINES)
        self.execute_query(CREATE_TABLE_HULLS)
        self.execute_query(CREATE_TABLE_SHIPS)

    def fill_db(self, required_number_of_ships: int, required_number_of_weapons: int,
                required_number_of_hulls: int, required_number_of_engines: int):
        """
        Method that fills database with random data
        :param required_number_of_ships: number of required ships
        :param required_number_of_weapons: number of required weapons
        :param required_number_of_hulls:  number of required hulls
        :param required_number_of_engines: number of required engines
        :return: None
        """
        created_weapons = []
        created_hulls = []
        created_engines = []
        for num in range(required_number_of_weapons):
            weapon = gen_part(WEAPON_NAME.format(num + 1), len(WEAPONS_TABLE_ROWS_NAMES))
            self.execute_query(INSERT_QUERY.format(table_name=WEAPONS_TABLE_NAME,
                                                   table_rows=(WEAPONS_TABLE_PRIMARY_KEY,) + WEAPONS_TABLE_ROWS_NAMES,
                                                   rows_values=weapon))
            created_weapons.append(weapon[0])
        for num in range(required_number_of_hulls):
            hull = gen_part(HULL_NAME.format(num + 1), len(HULLS_TABLE_ROWS_NAME))
            self.execute_query(INSERT_QUERY.format(table_name=HULLS_TABLE_NAME,
                                                   table_rows=(HULLS_TABLE_PRIMARY_KEY,) + HULLS_TABLE_ROWS_NAME,
                                                   rows_values=hull))
            created_hulls.append(hull[0])

        for num in range(required_number_of_engines):
            engine = gen_part(ENGINE_NAME.format(num + 1), len(ENGINES_TABLE_ROWS_NAME))
            self.execute_query(INSERT_QUERY.format(table_name=ENGINES_TABLE_NAME,
                                                   table_rows=(ENGINES_TABLE_PRIMARY_KEY,) + ENGINES_TABLE_ROWS_NAME,
                                                   rows_values=engine))
            created_engines.append(engine[0])

        for num in range(required_number_of_ships):
            ship = gen_ship(SHIP_NAME.format(num + 1), available_weapons=created_weapons,
                            available_hulls=created_hulls,
                            available_engines=created_engines)
            self.execute_query(INSERT_QUERY.format(table_name=SHIPS_TABLE_NAME,
                                                   table_rows=(SHIPS_TABLE_PRIMARY_KEY,) + SHIPS_TABLE_ROWS_NAME,
                                                   rows_values=ship))

    def copy_and_randomize_db(self):
        """
        Method that creates temporary copy of current database and randomizes values according to rules listed in task
        :return: instance of copied database
        """

        copied_db = self.create_temp_copy()
        weapons = copied_db.execute_query(SELECT_ALL_QUERY.format(table_name=WEAPONS_TABLE_NAME))
        available_weapons = []
        for weapon_data in weapons:
            random_property = random.choice(WEAPONS_TABLE_ROWS_NAMES)
            property_value = getattr(Weapon(*weapon_data), random_property)
            random_value = random.randint(*INTEGER_INTERVAL)
            while random_value == property_value:
                random_value = random.randint(*INTEGER_INTERVAL)
            copied_db.execute_query(
                UPDATE_QUERY.format(table_name=WEAPONS_TABLE_NAME, row_name=random_property,
                                    row_value=random_value,
                                    primary_key_name=WEAPONS_TABLE_PRIMARY_KEY, primary_key_value=weapon_data[0]))
            available_weapons.append(weapon_data[0])

        engines = copied_db.execute_query(SELECT_ALL_QUERY.format(table_name=ENGINES_TABLE_NAME))
        available_engines = []
        for engine_data in engines:
            random_property = random.choice(ENGINES_TABLE_ROWS_NAME)
            property_value = getattr(Engine(*engine_data), random_property)
            random_value = random.randint(*INTEGER_INTERVAL)
            while random_value == property_value:
                random_value = random.randint(*INTEGER_INTERVAL)
            copied_db.execute_query(
                UPDATE_QUERY.format(table_name=ENGINES_TABLE_NAME, row_name=random.choice(ENGINES_TABLE_ROWS_NAME),
                                    row_value=random.randint(*INTEGER_INTERVAL),
                                    primary_key_name=ENGINES_TABLE_PRIMARY_KEY, primary_key_value=engine_data[0]))
            available_engines.append(engine_data[0])

        hulls = copied_db.execute_query(SELECT_ALL_QUERY.format(table_name=HULLS_TABLE_NAME))
        available_hulls = []
        for hull_data in hulls:
            random_property = random.choice(HULLS_TABLE_ROWS_NAME)
            property_value = getattr(Hull(*hull_data), random_property)
            random_value = random.randint(*INTEGER_INTERVAL)
            while random_value == property_value:
                random_value = random.randint(*INTEGER_INTERVAL)
            copied_db.execute_query(
                UPDATE_QUERY.format(table_name=HULLS_TABLE_NAME, row_name=random.choice(HULLS_TABLE_ROWS_NAME),
                                    row_value=random.randint(*INTEGER_INTERVAL),
                                    primary_key_name=HULLS_TABLE_PRIMARY_KEY, primary_key_value=hull_data[0]))
            available_hulls.append(hull_data[0])

        available_parts_map = dict(zip(SHIPS_TABLE_ROWS_NAME, (available_weapons, available_hulls, available_engines)))
        ships = copied_db.execute_query(SELECT_ALL_QUERY.format(table_name=SHIPS_TABLE_NAME))
        for ship_data in ships:
            random_part = random.choice(SHIPS_TABLE_ROWS_NAME)
            random_part_name = random.choice(available_parts_map[random_part])
            while random_part_name in ship_data:
                random_part_name = random.choice(available_parts_map[random_part])
            copied_db.execute_query(UPDATE_QUERY.format(table_name=SHIPS_TABLE_NAME, row_name=random_part,
                                                        row_value=random_part_name,
                                                        primary_key_name=SHIPS_TABLE_PRIMARY_KEY,
                                                        primary_key_value=ship_data[0]))

        return copied_db

    def get_ship(self, ship_name):
        ship_query = SELECT_ROW_QUERY.format(table_name="ships", primary_key_name="ship", primary_key_value=ship_name)
        ship_data = self.execute_query(ship_query)[0]
        weapon_query = SELECT_ROW_QUERY.format(table_name="weapons", primary_key_name="weapon",
                                               primary_key_value=ship_data[1])
        weapon_data = self.execute_query(weapon_query)[0]
        hull_query = SELECT_ROW_QUERY.format(table_name="hulls", primary_key_name="hull",
                                             primary_key_value=ship_data[2])
        hull_data = self.execute_query(hull_query)[0]
        engine_query = SELECT_ROW_QUERY.format(table_name="engines", primary_key_name="engine",
                                               primary_key_value=ship_data[3])
        engine_data = self.execute_query(engine_query)[0]

        return Ship(ship_data[0], weapon_data, hull_data, engine_data)

    def get_ships_names(self):
        ships = self.execute_query(SELECT_ALL_QUERY.format(table_name=SHIPS_TABLE_NAME))
        return [ship_data[0] for ship_data in ships]
