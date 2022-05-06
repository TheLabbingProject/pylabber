import logging
from typing import List

import pandas as pd
from django.db import models
from external_tables.sync import logs
from external_tables.sync.synchronizer import Synchronizer
from research.models.subject import Subject


class SubjectsSynchronizer(Synchronizer):
    #: Database model to synchronize with dataframe.
    MODEL: models.Model = Subject

    #: Dataframe columns to synchronize with model fields.
    SYNC_FIELDS: List[str] = [
        "First Name",
        "Last Name",
        "Sex",
        "Date Of Birth",
    ]

    _logger = logging.getLogger("external_tables.sync")

    def clean_table(
        self, df: pd.DataFrame, log_level: int = logging.DEBUG,
    ) -> pd.DataFrame:
        """
        Cleans up the raw sheet parsing result.

        Parameters
        ----------
        df : pd.DataFrame
            Subjects dataframe from external table
        log_level : int, optional
            Level of logging to use, by default logging.DEBUG

        Returns
        -------
        pd.DataFrame
            Clean subjects dataframe
        """
        # Start log.
        start_log = logs.CLEANUP_START.format(
            model=self.MODEL.__name__.lower()
        )
        self._logger.log(log_level, start_log)
        # Remove flagged columns.
        flagged_columns = list(df.filter(regex=self.drop_column_flag))
        df = df[df.columns.drop(flagged_columns)].copy()
        # Log flagged columns removal.
        flagged_columns_log = logs.FLAGGED_COLUMNS_CLEANUP.format(
            n_flagged_columns=len(flagged_columns),
            drop_column_flag=self.drop_column_flag,
            flagged_columns=flagged_columns,
        )
        self._logger.log(log_level, flagged_columns_log)
        # Fix date of birth to use native Python date type.
        df.loc[:, "Date Of Birth"] = pd.to_datetime(
            df.loc[:, "Date Of Birth"], format="%d/%m/%Y"
        )
        # Drop rows with no :attr:`id_column` and reset the index to it.
        return df.dropna(subset=[self.id_column]).set_index(self.id_column)

    def sync_subject(self, row: pd.Series, dry: bool = False) -> None:
        """
        Synchronize database subject information from subject series.

        Parameters
        ----------
        row : pd.Series
            Subject row from subjects dataframe
        dry : bool, optional
            Whether to skip applying the changes, by default False
        """
        try:
            subject = Subject.objects.get(**{self.id_field: row.name})
        except Subject.DoesNotExist:
            # Warn table subject does not exist in the database.
            warning_log = logs.NO_DATABASE_INSTANCE.format(
                model_name=self.MODEL.__name__,
                field_name=self.id_field,
                value=row.name,
            )
            self._logger.log(logging.WARNING, warning_log)
        else:
            sync_fields = row[self.SYNC_FIELDS]
            updated = False
            for field_name, table_value in sync_fields.items():
                # Fix field names from column titles to model attributes.
                field_name = field_name.lower().replace(" ", "_")
                # Fix table values to match database values.
                if field_name == "date_of_birth":
                    table_value = table_value.date()
                elif field_name == "sex":
                    table_value = table_value[0]
                # Compare with current database value.
                db_value = getattr(subject, field_name)
                if db_value != table_value:
                    # Log update and flag as updated.
                    update_message = logs.FIELD_MISMATCH.format(
                        instance=subject,
                        field_name=field_name,
                        db_value=db_value,
                        table_value=table_value,
                    )
                    self._logger.log(logging.INFO, update_message)
                    setattr(subject, field_name, table_value)
                    updated = True
            if updated and not dry:
                subject.save()

    def sync(
        self,
        df: pd.DataFrame,
        dry: bool = False,
        log_level: int = logging.DEBUG,
    ) -> None:
        df = self.clean_table(df, log_level=log_level)
        df.apply(self.sync_subject, dry=dry, axis=1)
