from .conf import config


class SignupConfig:
    enable_conf_email: bool = config["signup"]["enable_conf_email"]
    conf_code_expiry: int = config["signup"]["conf_code_expiry"]
    conf_code_complexity: int = config["signup"]["conf_code_complexity"]
    enable_welcome_email: bool = config["signup"]["enable_welcome_email"]
    oauth_providers: list[str] = config["signup"]["oauth"]["providers_enabled"]
    oauth_base_url: str = str(config["signup"]["oauth"]["base_url"]).removesuffix("/")

    def validate_types(self) -> bool:
        """This is to Type Check the Configuration"""
        if not isinstance(self.enable_conf_email, bool):
            raise ValueError(
                "signup.enable_conf_email must be a boolean (got type {})".format(
                    type(self.enable_conf_email)
                )
            )
        if not isinstance(self.conf_code_expiry, int):
            raise ValueError(
                "signup.conf_code_expiry must be an integer (got type {})".format(
                    type(self.conf_code_expiry)
                )
            )
        if not isinstance(self.conf_code_complexity, int):
            raise ValueError(
                "signup.conf_code_complexity must be an integer (got type {})".format(
                    type(self.conf_code_complexity)
                )
            )
        if not isinstance(self.enable_welcome_email, bool):
            raise ValueError(
                "signup.enable_welcome_email must be a boolean (got type {})".format(
                    type(self.enable_welcome_email)
                )
            )
        if not isinstance(self.oauth_providers, list):
            raise ValueError(
                "signup.oauth.providers_enabled must be a list (got type {})".format(
                    type(self.oauth_providers)
                )
            )
        if not all(isinstance(i, str) for i in self.oauth_providers):
            raise ValueError("signup.oauth.providers_enabled must be a list of strings")
        if not isinstance(self.oauth_base_url, str):
            raise ValueError(
                "signup.oauth.base_url must be a string (got type {})".format(
                    type(self.oauth_base_url)
                )
            )
        pass


SignupConfig().validate_types()
