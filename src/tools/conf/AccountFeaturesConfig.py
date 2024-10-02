from .conf import config, not_updateable_cols_internal


class AccountFeaturesConfig:
    enable_reset_pswd: bool = config["account_features"]["enable_reset_pswd"]
    enable_2fa: bool = config["account_features"]["2fa"]["enable"]
    issuer_name_2fa: str = config["account_features"]["2fa"]["issuer_name"]
    issuer_image_url_2fa: str = config["account_features"]["2fa"]["issuer_image_url"]
    qr_code_endpoint_2fa: bool = config["account_features"]["2fa"]["qr_endpoint"]

    if not isinstance(config["account_features"]["allow_add_fields_on_signup"], list):
        raise ValueError(
            "account_features.allow_add_fields_on_signup must be a list (got type {})".format(
                type(config["account_features"]["allow_add_fields_on_signup"])
            )
        )

    allow_add_fields_on_signup: set[str] = set(
        config["account_features"]["allow_add_fields_on_signup"]
    ) - set(not_updateable_cols_internal)

    if not isinstance(config["account_features"]["allow_add_fields_patch_user"], list):
        raise ValueError(
            "account_features.allow_add_fields_patch_user must be a list (got type {})".format(
                type(config["account_features"]["allow_add_fields_patch_user"])
            )
        )

    allow_add_fields_patch_user: set[str] = set(
        config["account_features"]["allow_add_fields_patch_user"]
    ) - set(not_updateable_cols_internal)
    allow_deletion: bool = config["account_features"]["allow_deletion"]
    deletion_pending_minutes: int = config["account_features"][
        "deletion_pending_minutes"
    ]
    allow_profile_picture: bool = config["account_features"]["profile_picture"]["allow"]
    profile_picture_resize_width: int = config["account_features"]["profile_picture"][
        "resize"
    ]["width"]
    profile_picture_resize_height: int = config["account_features"]["profile_picture"][
        "resize"
    ]["height"]
    profile_picture_quality: int = config["account_features"]["profile_picture"][
        "quality"
    ]
    allow_gif: bool = config["account_features"]["profile_picture"]["allow_gif"]
    max_size_mb: float = config["account_features"]["profile_picture"]["max_size_mb"]
    max_gif_frames: int = config["account_features"]["profile_picture"][
        "max_gif_frames"
    ]

    def validate_types(self) -> bool:
        """This is to Type Check the Configuration"""
        if not isinstance(self.enable_reset_pswd, bool):
            raise ValueError(
                "account_features.enable_reset_pswd must be a boolean (got type {})".format(
                    type(self.enable_reset_pswd)
                )
            )
        if not isinstance(self.enable_2fa, bool):
            raise ValueError(
                "account_features.2fa.enable must be a boolean (got type {})".format(
                    type(self.enable_2fa)
                )
            )
        if not isinstance(self.issuer_name_2fa, str):
            raise ValueError(
                "account_features.2fa.issuer_name must be a string (got type {})".format(
                    type(self.issuer_name_2fa)
                )
            )
        if not isinstance(self.issuer_image_url_2fa, str):
            raise ValueError(
                "account_features.2fa.issuer_image_url must be a string (got type {})".format(
                    type(self.issuer_image_url_2fa)
                )
            )
        if not isinstance(self.qr_code_endpoint_2fa, bool):
            raise ValueError(
                "account_features.2fa.qr_endpoint must be a boolean (got type {})".format(
                    type(self.qr_code_endpoint_2fa)
                )
            )
        if not isinstance(self.allow_deletion, bool):
            raise ValueError(
                "account_features.allow_deletion must be a boolean (got type {})".format(
                    type(self.allow_deletion)
                )
            )
        if not isinstance(self.deletion_pending_minutes, int):
            raise ValueError(
                "account_features.deletion_pending_minutes must be an integer (got type {})".format(
                    type(self.deletion_pending_minutes)
                )
            )

        if not isinstance(self.allow_profile_picture, bool):
            raise ValueError(
                "account_features.allow_profile_picture must be a boolean (got type {})".format(
                    type(self.allow_profile_picture)
                )
            )

        if not isinstance(self.profile_picture_resize_width, int):
            raise ValueError(
                "account_features.profile_picture_resize.width must be an integer (got type {})".format(
                    type(self.profile_picture_resize_width)
                )
            )

        if not isinstance(self.profile_picture_resize_height, int):
            raise ValueError(
                "account_features.profile_picture_resize.height must be an integer (got type {})".format(
                    type(self.profile_picture_resize_height)
                )
            )

        if not isinstance(self.profile_picture_quality, int):
            raise ValueError(
                "account_features.profile_picture.quality must be an integer (got type {})".format(
                    type(self.profile_picture_quality)
                )
            )

        if not isinstance(self.allow_gif, bool):
            raise ValueError(
                "account_features.profile_picture.allow_gif must be a boolean (got type {})".format(
                    type(self.allow_gif)
                )
            )

        if not isinstance(self.max_size_mb, (float, int)):
            raise ValueError(
                "account_features.profile_picture.max_size_mb must be a float (got type {})".format(
                    type(self.max_size_mb)
                )
            )

        if not isinstance(self.max_gif_frames, int):
            raise ValueError(
                "account_features.profile_picture.max_gif_frames must be an integer (got type {})".format(
                    type(self.max_gif_frames)
                )
            )

    def validate_values(self) -> bool:
        """This is to Value Check the Configuration"""
        if not self.issuer_name_2fa:
            raise ValueError("account_features.2fa.issuer_name must not be empty")
        if not self.deletion_pending_minutes > 0:
            raise ValueError(
                "account_features.deletion_pending_minutes must be a positive integer (got {})".format(
                    self.deletion_pending_minutes
                )
            )

        if not self.profile_picture_resize_width > 0:
            raise ValueError(
                "account_features.profile_picture_resize.width must be a positive integer (got {})".format(
                    self.profile_picture_resize_width
                )
            )

        if not self.profile_picture_resize_height > 0:
            raise ValueError(
                "account_features.profile_picture_resize.height must be a positive integer (got {})".format(
                    self.profile_picture_resize_height
                )
            )

        if not 0 < self.profile_picture_quality <= 100:
            raise ValueError(
                "account_features.profile_picture.quality must be an integer between 1 and 100 (got {})".format(
                    self.profile_picture_quality
                )
            )

        if not self.max_size_mb > 0:
            raise ValueError(
                "account_features.profile_picture.max_size_mb must be a positive float (got {})".format(
                    self.max_size_mb
                )
            )

        if not self.max_gif_frames > 0:
            raise ValueError(
                "account_features.profile_picture.max_gif_frames must be a positive integer (got {})".format(
                    self.max_gif_frames
                )
            )


AccountFeaturesConfig().validate_types()
AccountFeaturesConfig().validate_values()
