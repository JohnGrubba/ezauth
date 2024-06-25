import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from . import EmailConfig
import logging


def load_template(template_name: str, **kwargs) -> str:
    with open(f"/src/app/config/email/{template_name}.html", "r") as file:
        template = file.read()
    subject = template[template.find("<title>") + 7 : template.find("</title>")]
    return template.format(**kwargs), subject


def send_email(template_name: str, to: str, **kwargs):
    html_content, subject = load_template(template_name, **kwargs)

    msg = MIMEMultipart()
    msg["From"] = EmailConfig.sender_email
    msg["To"] = to
    msg["Subject"] = subject

    # Attach HTML content
    msg.attach(MIMEText(html_content, "html"))

    # Send email
    with smtplib.SMTP_SSL(EmailConfig.smtp_host, EmailConfig.smtp_port) as server:
        server.login(EmailConfig.login_usr, EmailConfig.login_pwd)
        server.send_message(msg)

    logging.info(f"Email sent to {to} with subject: {subject}")
