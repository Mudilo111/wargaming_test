from models.base_model import BaseModel
from sql_utilites.sql_constants import HULLS_TABLE_ROWS_NAME


class Hull(BaseModel):

    def __init__(self, *args):
        super().__init__(args[0], HULLS_TABLE_ROWS_NAME, args[1:])
