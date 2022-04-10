from models.base_model import BaseModel
from sql_utilites.sql_constants import WEAPONS_TABLE_ROWS_NAMES


class Weapon(BaseModel):

    def __init__(self, *args):
        super().__init__(args[0], WEAPONS_TABLE_ROWS_NAMES, args[1:])
