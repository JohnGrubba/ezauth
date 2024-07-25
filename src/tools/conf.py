import json
from collections import ChainMap
import sys
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

if "pytest" in sys.modules:
    # Running Tests (Load Testing Config)
    config = json.load(open(os.path.join(__location__, "testing_config.json"), "rb"))
else:
    # Normal Startup
    config = json.load(open("/src/app/config/config.json", "rb"))

# Columns that should never leave EZAuth (maybe get more in the future)
default_signup_fields = {"username", "email", "password"}
insecure_cols = {"password": 0, "2fa_secret": 0, "google_uid": 0, "github_uid": 0}
not_updateable_cols_internal = ["email", "createdAt", "expireAt"]
# Columns that can leave EZAuth but should only be used internally can be defined in config


class SignupConfig:
    enable_conf_email: bool = config["signup"]["enable_conf_email"]
    conf_code_expiry: int = config["signup"]["conf_code_expiry"]
    conf_code_complexity: int = config["signup"]["conf_code_complexity"]
    enable_welcome_email: bool = config["signup"]["enable_welcome_email"]
    oauth_providers: list[str] = config["signup"]["oauth"]["providers_enabled"]
    oauth_base_url: str = str(config["signup"]["oauth"]["base_url"]).removesuffix("/")
    password_complexity: int = config["signup"]["password_complexity"]
    username_complexity: int = config["signup"]["username_complexity"]


class EmailConfig:
    login_usr: str = config["email"]["login_usr"]
    login_pwd: str = config["email"]["login_pwd"]
    sender_email: str = config["email"]["sender_email"]
    smtp_host: str = config["email"]["smtp_host"]
    smtp_port: int = config["email"]["smtp_port"]


class SessionConfig:
    session_expiry_seconds: int = config["session"]["session_expiry_seconds"]
    max_session_count: int = config["session"]["max_session_count"]
    auto_cookie: bool = config["session"]["auto_cookie"]
    auto_cookie_name: str = config["session"]["auto_cookie_name"]
    cookie_samesite: str = config["session"]["cookie_samesite"]
    cookie_secure: bool = config["session"]["cookie_secure"]


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


class SecurityConfig:
    access_control_origins: set[str] = set(config["security"]["allow_origins"])
    allow_headers: set[str] = set(config["security"]["allow_headers"])
    max_login_attempts: int = config["security"]["max_login_attempts"]
    login_timeout: int = config["security"]["login_timeout"]
    expire_unfinished_timeout: int = config["security"]["expire_unfinished_timeout"]
