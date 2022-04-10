import pytest
from tets_data.constants import SHIP_NAME
from sql_utilites.sql_constants import SHIPS_TABLE_ROWS_NAME


class TestShipsDB:

    @pytest.mark.parametrize('part', [*SHIPS_TABLE_ROWS_NAME])
    def test_ship_part(self, setup_env, ship_number, part):
        initial_db, copied_db = setup_env
        initial_ship = initial_db.get_ship(SHIP_NAME.format(ship_number))
        copied_db = copied_db.get_ship(SHIP_NAME.format(ship_number))
        comparison_result = initial_ship.compare_ships_parts(part, copied_db)
        assert not comparison_result, comparison_result
