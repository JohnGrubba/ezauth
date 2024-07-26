from .conf import config, not_updateable_cols_internal


class AccountFeaturesConfig:
    enable_reset_pswd: bool = config["account_features"]["enable_reset_pswd"]
    reset_pswd_conf_mail: bool = config["account_features"]["reset_pswd_conf_mail"]
    enable_2fa: bool = config["account_features"]["2fa"]["enable"]
    issuer_name_2fa: str = config["account_features"]["2fa"]["issuer_name"]
    issuer_image_url_2fa: str = config["account_features"]["2fa"]["issuer_image_url"]
    qr_code_endpoint_2fa: bool = config["account_features"]["2fa"]["qr_endpoint"]
    allow_add_fields_on_signup: set[str] = set(
        config["account_features"]["allow_add_fields_on_signup"]
    ) - set(not_updateable_cols_internal)
    allow_add_fields_patch_user: set[str] = set(
        config["account_features"]["allow_add_fields_patch_user"]
    ) - set(not_updateable_cols_internal)
    allow_deletion: bool = config["account_features"]["allow_deletion"]
    deletion_pending_minutes: int = config["account_features"][
        "deletion_pending_minutes"
    ]
