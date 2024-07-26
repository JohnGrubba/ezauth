from .conf import config, insecure_cols, not_updateable_cols_internal
from collections import ChainMap


class InternalConfig:
    internal_api_key: str = config["internal"]["internal_api_key"]
    # Type Check here because calculations need to be done immediately
    if not isinstance(config["internal"]["internal_columns"], list):
        raise ValueError(
            "internal.internal_columns must be a list (got type {})".format(
                type(config["internal"]["internal_columns"])
            )
        )
    internal_columns: dict = dict(
        ChainMap(*[{col: 0} for col in set(config["internal"]["internal_columns"])])
    )
    internal_columns.update(insecure_cols)
    # Insecure Cols + Internal Cols can't be updated by the user
    if not isinstance(config["internal"]["not_updateable_columns"], list):
        raise ValueError(
            "internal.not_updateable_columns must be a list (got type {})".format(
                type(config["internal"]["not_updateable_columns"])
            )
        )
    not_updateable_columns: set = set(
        config["internal"]["not_updateable_columns"]
        + list(internal_columns.keys())
        + not_updateable_cols_internal
    )

    def validate_types(self) -> bool:
        """This is to Type Check the Configuration"""
        if not isinstance(self.internal_api_key, str):
            raise ValueError(
                "internal.internal_api_key must be a string (got type {})".format(
                    type(self.internal_api_key)
                )
            )


InternalConfig().validate_types()
