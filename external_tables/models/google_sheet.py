"""
Definition of the :class:`GoogleSheet` model.
"""
import logging

import pandas as pd
from django.db import models
from external_tables.models.sync_table import SyncTable
from external_tables.sync.synchronizer import Synchronizer
from external_tables.sync.utils import MODEL_SYNCHRONIZER


class GoogleSheet(SyncTable):
    #: URL pattern used to export Google Sheet documents to CSV and read with
    #: pandas.
    URL_PATTERN: str = "https://docs.google.com/spreadsheets/d/{key}/gviz/tq?tqx=out:csv&sheet={sheet_name}"  # noqa: E501

    #: Google Sheets document key.
    key = models.CharField(max_length=255, blank=False, null=False)

    #: Sheet name.
    sheet_name = models.CharField(max_length=255, blank=False, null=False)

    # Synchronizer instance cache.
    _synchronizer: Synchronizer = None

    def read_table(self) -> pd.DataFrame:
        url = self.URL_PATTERN.format(key=self.key, sheet_name=self.sheet_name)
        return pd.read_csv(url, dtype={self.id_column: str})

    def get_synchronizer(self) -> Synchronizer:
        label = f"{self.content_type.app_labeled_name}"
        try:
            return MODEL_SYNCHRONIZER[label]
        except KeyError:
            raise NotImplementedError("Synchronizer for {label} not found!")

    def sync(self, dry: bool = False, log_level: int = logging.DEBUG) -> None:
        self.synchronizer.sync(self.df, dry=dry, log_level=log_level)

    @property
    def synchronizer(self) -> Synchronizer:
        if self._synchronizer is None:
            SynchronizerSubclass = self.get_synchronizer()
            self._synchronizer = SynchronizerSubclass(
                id_column=self.id_column, id_field=self.id_field
            )
        return self._synchronizer
