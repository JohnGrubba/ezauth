from .conf import config


class SecurityConfig:
    access_control_origins: set[str] = set(config["security"]["allow_origins"])
    allow_headers: set[str] = set(config["security"]["allow_headers"])
    max_login_attempts: int = config["security"]["max_login_attempts"]
    login_timeout: int = config["security"]["login_timeout"]
    expire_unfinished_timeout: int = config["security"]["expire_unfinished_timeout"]
