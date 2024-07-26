from .conf import config, not_updateable_cols_internal


class AccountFeaturesConfig:
    enable_reset_pswd: bool = config["account_features"]["enable_reset_pswd"]
    reset_pswd_conf_mail: bool = config["account_features"]["reset_pswd_conf_mail"]
    enable_2fa: bool = config["account_features"]["2fa"]["enable"]
    issuer_name_2fa: str = config["account_features"]["2fa"]["issuer_name"]
    issuer_image_url_2fa: str = config["account_features"]["2fa"]["issuer_image_url"]
    qr_code_endpoint_2fa: bool = config["account_features"]["2fa"]["qr_endpoint"]

    if not isinstance(config["account_features"]["allow_add_fields_on_signup"], list):
        raise ValueError(
            "account_features.allow_add_fields_on_signup must be a list (got type {})".format(
                type(config["account_features"]["allow_add_fields_on_signup"])
            )
        )

    allow_add_fields_on_signup: set[str] = set(
        config["account_features"]["allow_add_fields_on_signup"]
    ) - set(not_updateable_cols_internal)

    if not isinstance(config["account_features"]["allow_add_fields_patch_user"], list):
        raise ValueError(
            "account_features.allow_add_fields_patch_user must be a list (got type {})".format(
                type(config["account_features"]["allow_add_fields_patch_user"])
            )
        )

    allow_add_fields_patch_user: set[str] = set(
        config["account_features"]["allow_add_fields_patch_user"]
    ) - set(not_updateable_cols_internal)
    allow_deletion: bool = config["account_features"]["allow_deletion"]
    deletion_pending_minutes: int = config["account_features"][
        "deletion_pending_minutes"
    ]

    def validate_types(self) -> bool:
        """This is to Type Check the Configuration"""
        if not isinstance(self.enable_reset_pswd, bool):
            raise ValueError(
                "account_features.enable_reset_pswd must be a boolean (got type {})".format(
                    type(self.enable_reset_pswd)
                )
            )
        if not isinstance(self.reset_pswd_conf_mail, bool):
            raise ValueError(
                "account_features.reset_pswd_conf_mail must be a boolean (got type {})".format(
                    type(self.reset_pswd_conf_mail)
                )
            )
        if not isinstance(self.enable_2fa, bool):
            raise ValueError(
                "account_features.2fa.enable must be a boolean (got type {})".format(
                    type(self.enable_2fa)
                )
            )
        if not isinstance(self.issuer_name_2fa, str):
            raise ValueError(
                "account_features.2fa.issuer_name must be a string (got type {})".format(
                    type(self.issuer_name_2fa)
                )
            )
        if not isinstance(self.issuer_image_url_2fa, str):
            raise ValueError(
                "account_features.2fa.issuer_image_url must be a string (got type {})".format(
                    type(self.issuer_image_url_2fa)
                )
            )
        if not isinstance(self.qr_code_endpoint_2fa, bool):
            raise ValueError(
                "account_features.2fa.qr_endpoint must be a boolean (got type {})".format(
                    type(self.qr_code_endpoint_2fa)
                )
            )
        if not isinstance(self.allow_deletion, bool):
            raise ValueError(
                "account_features.allow_deletion must be a boolean (got type {})".format(
                    type(self.allow_deletion)
                )
            )
        if not isinstance(self.deletion_pending_minutes, int):
            raise ValueError(
                "account_features.deletion_pending_minutes must be an integer (got type {})".format(
                    type(self.deletion_pending_minutes)
                )
            )


AccountFeaturesConfig().validate_types()
