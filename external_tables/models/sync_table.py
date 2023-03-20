"""
Definition of the :class:`SyncTable` class.
"""
import pandas as pd
from django.contrib.contenttypes.models import ContentType
from django.db import models


class SyncTable(models.Model):
    #: The database model to be synchronized with the information in the table.
    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=False, null=False
    )
    #: The table column to be used to query database rows.
    id_column = models.CharField(
        max_length=128, blank=False, null=False, default="ID"
    )
    #: The model field to query :attr:`id_column` against.
    id_field = models.CharField(
        max_length=128, blank=False, null=False, default="id"
    )

    # Cached table `DataFrame` instance.
    _df: pd.DataFrame = None

    class Meta:
        abstract = True

    def read_table(self) -> pd.DataFrame:
        """
        Reads the table from a specified location.

        This method is meant to be overridden by subclasses and implemented
        according to the table's location and format.

        Returns
        -------
        pd.DataFrame
            Table data

        Raises
        ------
        NotImplementedError
            Method must be implemented by subclasses
        """
        raise NotImplementedError

    def sync(self) -> None:
        """
        Synchronizes the database with the information stored in this table.

        Raises
        ------
        NotImplementedError
            Method must be implemented by subclasses
        """
        raise NotImplementedError

    @property
    def df(self) -> pd.DataFrame:
        """
        Returns the :class:`SyncTable` as a dataframe.

        Returns
        -------
        pd.DataFrame
            Table information
        """
        if self._df is None:
            self._df = self.read_table()
        return self._df
