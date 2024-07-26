from .conf import config


class SecurityConfig:
    access_control_origins: set[str] = config["security"]["allow_origins"]
    allow_headers: set[str] = config["security"]["allow_headers"]
    max_login_attempts: int = config["security"]["max_login_attempts"]
    login_timeout: int = config["security"]["login_timeout"]
    expire_unfinished_timeout: int = config["security"]["expire_unfinished_timeout"]

    def validate_types(self) -> bool:
        """This is to Type Check the Configuration"""
        if not isinstance(self.access_control_origins, list):
            self.access_control_origins = set(self.access_control_origins)
            raise ValueError(
                "security.allow_origins must be a list (got type {})".format(
                    type(self.access_control_origins)
                )
            )
        if not isinstance(self.allow_headers, list):
            self.allow_headers = set(self.allow_headers)
            raise ValueError(
                "security.allow_headers must be a list (got type {})".format(
                    type(self.allow_headers)
                )
            )
        if not isinstance(self.max_login_attempts, int):
            raise ValueError(
                "security.max_login_attempts must be an integer (got type {})".format(
                    type(self.max_login_attempts)
                )
            )
        if not isinstance(self.login_timeout, int):
            raise ValueError(
                "security.login_timeout must be an integer (got type {})".format(
                    type(self.login_timeout)
                )
            )
        if not isinstance(self.expire_unfinished_timeout, int):
            raise ValueError(
                "security.expire_unfinished_timeout must be an integer (got type {})".format(
                    type(self.expire_unfinished_timeout)
                )
            )


SecurityConfig().validate_types()
