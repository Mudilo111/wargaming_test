import pytest
from sql_utilites.ships_db_session import ShipsDBSession
from tets_data.constants import DEFAULT_DB_NAME, DEFAULT_NUMBER_OF_SHIPS, DEFAULT_NUMBER_OF_ENGINES, \
    DEFAULT_NUMBER_OF_HULLS, DEFAULT_NUMBER_OF_WEAPONS

import pathlib
import os


def pytest_addoption(parser):
    parser.addoption("--db_name", action="store", default=DEFAULT_DB_NAME, help="Desired database name")
    parser.addoption("--number_of_ships", action="store", default=DEFAULT_NUMBER_OF_SHIPS,
                     help="Required number of ships")
    parser.addoption("--number_of_weapons", action="store", default=DEFAULT_NUMBER_OF_WEAPONS,
                     help="Required number of weapons")
    parser.addoption("--number_of_engines", action="store", default=DEFAULT_NUMBER_OF_ENGINES,
                     help="Required number of engines")
    parser.addoption("--number_of_hulls", action="store", default=DEFAULT_NUMBER_OF_HULLS,
                     help="Required number of hulls")


@pytest.fixture(scope="session")
def setup_env(pytestconfig):
    path_to_database = str(pathlib.Path().resolve()) + '\\' + pytestconfig.getoption('db_name')
    if os.path.exists(path_to_database):
        os.remove(path_to_database)
    initial_database = ShipsDBSession(path_to_database)
    initial_database.create_tables()
    initial_database.fill_db(required_number_of_ships=pytestconfig.getoption('number_of_ships'),
                             required_number_of_weapons=pytestconfig.getoption('number_of_weapons'),
                             required_number_of_hulls=pytestconfig.getoption('number_of_hulls'),
                             required_number_of_engines=pytestconfig.getoption('number_of_engines'))
    copied_database = initial_database.copy_and_randomize_db()
    yield initial_database, copied_database
    initial_database.session_end()
    copied_database.session_end()
    if os.path.exists(path_to_database):
        os.remove(path_to_database)


def pytest_generate_tests(metafunc):
    metafunc.parametrize('ship_number', range(1, metafunc.config.getoption('number_of_ships')+1))
