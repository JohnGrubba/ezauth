from .conf import config


class SignupConfig:
    enable_conf_email: bool = config["signup"]["enable_conf_email"]
    conf_code_expiry: int = config["signup"]["conf_code_expiry"]
    conf_code_complexity: int = config["signup"]["conf_code_complexity"]
    enable_welcome_email: bool = config["signup"]["enable_welcome_email"]
    oauth_providers: list[str] = config["signup"]["oauth"]["providers_enabled"]
    oauth_base_url: str = str(config["signup"]["oauth"]["base_url"]).removesuffix("/")

    def validate(self) -> bool:
        """This is to Type Check the Configuration

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            bool: _description_
        """
        if type(self.enable_conf_email) != bool:
            raise ValueError(
                "signup.enable_conf_email must be a boolean (got type {})".format(
                    type(self.enable_conf_email)
                )
            )
        if type(self.conf_code_expiry) != int:
            raise ValueError(
                "signup.conf_code_expiry must be an integer (got type {})".format(
                    type(self.conf_code_expiry)
                )
            )
        pass
