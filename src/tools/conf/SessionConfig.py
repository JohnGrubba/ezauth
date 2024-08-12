from .conf import config


class SessionConfig:
    session_expiry_seconds: int = config["session"]["session_expiry_seconds"]
    session_refresh_seconds: int = config["session"]["session_refresh_seconds"]
    max_session_count: int = config["session"]["max_session_count"]
    auto_cookie: bool = config["session"]["auto_cookie"]
    auto_cookie_name: str = config["session"]["auto_cookie_name"]
    cookie_samesite: str = config["session"]["cookie_samesite"]
    cookie_secure: bool = config["session"]["cookie_secure"]

    def validate_types(self) -> bool:
        """This is to Type Check the Configuration"""
        if not isinstance(self.session_expiry_seconds, int):
            raise ValueError(
                "session.session_expiry_seconds must be an integer (got type {})".format(
                    type(self.session_expiry_seconds)
                )
            )
        if not isinstance(self.session_refresh_seconds, int):
            raise ValueError(
                "session.session_refresh_seconds must be an integer (got type {})".format(
                    type(self.session_refresh_seconds)
                )
            )
        if not isinstance(self.max_session_count, int):
            raise ValueError(
                "session.max_session_count must be an integer (got type {})".format(
                    type(self.max_session_count)
                )
            )
        if not isinstance(self.auto_cookie, bool):
            raise ValueError(
                "session.auto_cookie must be a boolean (got type {})".format(
                    type(self.auto_cookie)
                )
            )
        if not isinstance(self.auto_cookie_name, str):
            raise ValueError(
                "session.auto_cookie_name must be a string (got type {})".format(
                    type(self.auto_cookie_name)
                )
            )
        if not isinstance(self.cookie_samesite, str):
            raise ValueError(
                "session.cookie_samesite must be a string (got type {})".format(
                    type(self.cookie_samesite)
                )
            )
        if not isinstance(self.cookie_secure, bool):
            raise ValueError(
                "session.cookie_secure must be a boolean (got type {})".format(
                    type(self.cookie_secure)
                )
            )

    def validate_values(self) -> bool:
        """This is to Value Check the Configuration"""
        if not self.session_expiry_seconds > 0:
            raise ValueError(
                "session.session_expiry_seconds must be a positive integer (got {})".format(
                    self.session_expiry_seconds
                )
            )
        if not self.session_refresh_seconds > 0:
            raise ValueError(
                "session.session_refresh_seconds must be a positive integer (got {})".format(
                    self.session_refresh_seconds
                )
            )
        if self.session_refresh_seconds > self.session_expiry_seconds:
            raise ValueError(
                "session.session_refresh_seconds must be less or equal than session.session_expiry_seconds"
            )
        if not self.max_session_count > 0:
            raise ValueError(
                "session.max_session_count must be a positive integer (got {})".format(
                    self.max_session_count
                )
            )
        if self.auto_cookie and self.auto_cookie_name == "":
            raise ValueError(
                "session.auto_cookie_name must not be an empty string, when enabled"
            )
        if self.cookie_samesite not in ["strict", "lax", "none"]:
            raise ValueError(
                "session.cookie_samesite must be one of 'strict', 'lax', or 'none' (got {})".format(
                    self.cookie_samesite
                )
            )


SessionConfig().validate_types()
SessionConfig().validate_values()
