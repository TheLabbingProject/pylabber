import logging
from typing import List, Tuple

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
    CUSTOM_ATTRIBUTES: List[Tuple[str, str]] = [("Questionnaire ID", "String")]

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

    def sync_subject(
        self, row: pd.Series, dry: bool = False, warn_missing: bool = True
    ) -> None:
        """
        Synchronize database subject information from subject series.

        Parameters
        ----------
        row : pd.Series
            Subject row from subjects dataframe
        dry : bool, optional
            Whether to skip applying the changes, by default False
        warn_missing : bool, optional
            Whether to display a warning for missing database instances, by
            default False
        """
        try:
            subject = Subject.objects.get(**{self.id_field: row.name})
        except Subject.DoesNotExist:
            if warn_missing:
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
                if isinstance(table_value, str):
                    table_value = table_value.strip()
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
            for attribute_name, attribute_type in self.CUSTOM_ATTRIBUTES:
                value = row[attribute_name]
                if pd.isnull(value):
                    continue
                attribute_name = (
                    attribute_name.strip().lower().replace(" ", "_")
                )
                if attribute_name not in subject.custom_attributes:
                    subject.custom_attributes[attribute_name] = {
                        "type": attribute_type,
                        "value": value,
                    }
                    message = logs.CUSTOM_ATTRIBUTE_CREATION.format(
                        subject_id=subject.id, name=attribute_name, value=value
                    )
                    self._logger.log(logging.INFO, message)
                    updated = True
                elif (
                    subject.custom_attributes[attribute_name]["value"] != value
                ):
                    subject.custom_attributes[attribute_name] = {
                        "type": attribute_type,
                        "value": value,
                    }
                    message = logs.CUSTOM_ATTRIBUTE_UPDATE.format(
                        subject_id=subject.id, name=attribute_name, value=value
                    )
                    self._logger.log(logging.INFO, message)
                    updated = True
            if updated and not dry:
                subject.save()

    def sync(
        self,
        df: pd.DataFrame,
        dry: bool = False,
        log_level: int = logging.DEBUG,
        warn_missing: bool = False,
    ) -> None:
        df = self.clean_table(df, log_level=log_level)
        df.apply(self.sync_subject, dry=dry, warn_missing=warn_missing, axis=1)
