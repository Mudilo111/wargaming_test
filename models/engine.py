from models.base_model import BaseModel
from sql_utilites.sql_constants import ENGINES_TABLE_ROWS_NAME


class Engine(BaseModel):

    def __init__(self, *args):
        super().__init__(args[0], ENGINES_TABLE_ROWS_NAME, args[1:])
