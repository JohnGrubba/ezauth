from .conf import config, insecure_cols, not_updateable_cols_internal
from collections import ChainMap


class InternalConfig:
    internal_api_key: str = config["internal"]["internal_api_key"]
    internal_columns: dict = dict(
        ChainMap(*[{col: 0} for col in config["internal"]["internal_columns"]])
    )
    internal_columns.update(insecure_cols)
    # Insecure Cols + Internal Cols can't be updated by the user
    not_updateable_columns: list = (
        config["internal"]["not_updateable_columns"]
        + list(internal_columns.keys())
        + not_updateable_cols_internal
    )
