"""
Definition of the :class:`Synchronizer` base class.
"""
import logging

import pandas as pd
from django.db import models


class Synchronizer:
    #: The database model to be synchronized.
    MODEL: models.Model = None

    def __init__(
        self,
        id_column: str = "ID",
        id_field: str = "id",
        drop_column_flag: str = "Unnamed",
    ) -> None:
        self.id_column = id_column
        self.id_field = id_field
        self.drop_column_flag = drop_column_flag

    def sync(
        self,
        df: pd.DataFrame,
        dry: bool = False,
        log_level: int = logging.DEBUG,
    ) -> None:
        raise NotImplementedError

