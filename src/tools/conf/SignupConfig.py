from .conf import config


class SignupConfig:
    allow_signup: bool = config["signup"]["allow_signup"]
    enable_conf_email: bool = config["signup"]["enable_conf_email"]
    conf_code_expiry: int = config["signup"]["conf_code_expiry"]
    conf_code_complexity: int = config["signup"]["conf_code_complexity"]
    enable_welcome_email: bool = config["signup"]["enable_welcome_email"]
    oauth_providers: set[str] = config["signup"]["oauth"]["providers_enabled"]
    oauth_base_url: str = str(config["signup"]["oauth"]["base_url"]).removesuffix("/")
    oauth_redirect_url: str = str(
        config["signup"]["oauth"]["redirect_url"]
    ).removesuffix("/")
    password_complexity: int = config["signup"]["password_complexity"]
    username_complexity: int = config["signup"]["username_complexity"]

    def validate_types(self) -> bool:
        """This is to Type Check the Configuration"""
        if not isinstance(self.allow_signup, bool):
            raise ValueError(
                "signup.allow_signup must be a boolean (got type {})".format(
                    type(self.allow_signup)
                )
            )
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
            self.oauth_providers = set(self.oauth_providers)
            raise ValueError(
                "signup.oauth.providers_enabled must be a list (got type {})".format(
                    type(self.oauth_providers)
                )
            )
        if not all(isinstance(i, str) for i in self.oauth_providers):
            raise ValueError("signup.oauth.providers_enabled must be a list of strings")
        if not isinstance(self.password_complexity, int):
            raise ValueError(
                "signup.password_complexity must be an integer (got type {})".format(
                    type(self.password_complexity)
                )
            )
        if not isinstance(self.username_complexity, int):
            raise ValueError(
                "signup.username_complexity must be an integer (got type {})".format(
                    type(self.username_complexity)
                )
            )

    def validate_values(self) -> bool:
        """This is to Value Check the Configuration"""
        if not self.conf_code_expiry > 0:
            raise ValueError(
                f"signup.conf_code_expiry must be greater than 0, got {self.conf_code_expiry}"
            )
        if self.conf_code_complexity not in range(1, 5):
            raise ValueError(
                f"signup.conf_code_complexity must be between 1 and 4 (Check Docs), got {self.conf_code_complexity}"
            )
        if (
            len(self.oauth_providers) > 0
            and not self.oauth_base_url
            and "http" not in self.oauth_base_url
        ):
            raise ValueError(
                f"signup.oauth.base_url cannot be empty or malformed when OAuth is enabled, got {self.oauth_base_url}"
            )
        if self.oauth_redirect_url and "http" not in self.oauth_redirect_url:
            raise ValueError(
                f"signup.oauth.redirect_url must be a valid URL or empty, got {self.oauth_redirect_url}"
            )
        if self.password_complexity not in range(1, 5):
            raise ValueError(
                f"signup.password_complexity must be between 1 and 4 (Check Docs), got {self.password_complexity}"
            )
        if self.username_complexity not in range(1, 3):
            raise ValueError(
                f"signup.username_complexity must be 1 or 2 (Check Docs), got {self.username_complexity}"
            )


SignupConfig().validate_types()
SignupConfig().validate_values()
