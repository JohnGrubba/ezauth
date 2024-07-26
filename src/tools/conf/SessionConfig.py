from .conf import config


class SessionConfig:
    session_expiry_seconds: int = config["session"]["session_expiry_seconds"]
    max_session_count: int = config["session"]["max_session_count"]
    auto_cookie: bool = config["session"]["auto_cookie"]
    auto_cookie_name: str = config["session"]["auto_cookie_name"]
    cookie_samesite: str = config["session"]["cookie_samesite"]
    cookie_secure: bool = config["session"]["cookie_secure"]
