CLEANUP_START: str = "Cleaning up {model} dataframe..."
FLAGGED_COLUMNS_CLEANUP: str = "Removed {n_flagged_columns} columns flagged with {drop_column_flag}: {flagged_columns}"
NO_DATABASE_INSTANCE: str = "No {model_name} instance with {field_name} = {value} found! Skipping..."
FIELD_MISMATCH: str = "Database value for {instance}'s {field_name} field value is {db_value}, updating to {table_value}."

# flake8: noqa: E501
