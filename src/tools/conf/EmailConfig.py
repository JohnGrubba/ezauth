from .conf import config


class EmailConfig:
    login_usr: str = config["email"]["login_usr"]
    login_pwd: str = config["email"]["login_pwd"]
    sender_email: str = config["email"]["sender_email"]
    smtp_host: str = config["email"]["smtp_host"]
    smtp_port: int = config["email"]["smtp_port"]

    def validate_types(self) -> None:
        """This is to Type Check the Configuration"""
        if not isinstance(self.login_usr, str):
            raise ValueError(
                "email.login_usr must be a string (got type {})".format(
                    type(self.login_usr)
                )
            )
        if not isinstance(self.login_pwd, str):
            raise ValueError(
                "email.login_pwd must be a string (got type {})".format(
                    type(self.login_pwd)
                )
            )
        if not isinstance(self.sender_email, str):
            raise ValueError(
                "email.sender_email must be a string (got type {})".format(
                    type(self.sender_email)
                )
            )
        if not isinstance(self.smtp_host, str):
            raise ValueError(
                "email.smtp_host must be a string (got type {})".format(
                    type(self.smtp_host)
                )
            )
        if not isinstance(self.smtp_port, int):
            raise ValueError(
                "email.smtp_port must be an integer (got type {})".format(
                    type(self.smtp_port)
                )
            )

    def validate_values(self) -> None:
        """This is to Value Check the Configuration"""
        if self.sender_email and "@" not in self.sender_email:
            raise ValueError(
                "email.sender_email must contain a valid email address.\
                    This also works: `Test <test@test.com>` (got {})".format(
                    self.sender_email
                )
            )
        if self.smtp_host.startswith("http"):
            raise ValueError(
                "email.smtp_host must not contain `http` or `https` or `smtp` (got {})".format(
                    self.smtp_host
                )
            )
        if not 0 < self.smtp_port < 65536:
            raise ValueError(
                "email.smtp_port must be a valid port number (got {})".format(
                    self.smtp_port
                )
            )


EmailConfig().validate_types()
EmailConfig().validate_values()
