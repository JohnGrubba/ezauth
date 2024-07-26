from .conf import config


class EmailConfig:
    login_usr: str = config["email"]["login_usr"]
    login_pwd: str = config["email"]["login_pwd"]
    sender_email: str = config["email"]["sender_email"]
    smtp_host: str = config["email"]["smtp_host"]
    smtp_port: int = config["email"]["smtp_port"]
