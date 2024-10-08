import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .conf import EmailConfig
import logging
from threading import Lock
from tools import users_collection, InternalConfig
import importlib


def load_template(template_name: str, **kwargs) -> str:
    with open(f"/src/app/config/email/{template_name}.html", "r") as file:
        template = file.read()
    subject = template[template.find("<title>") + 7 : template.find("</title>")]
    # Try to find template_name + ".py" and execute the function "preprocess"
    try:
        module = importlib.import_module(f"config.email.{template_name}")
    except ModuleNotFoundError:
        pass
    else:
        logging.info(f"Found preprocess function in {template_name}.py")
        if hasattr(module, "preprocess"):
            logging.info(f"Executing preprocess function in {template_name}.py")
            try:
                kwargs = module.preprocess(kwargs)
            except Exception as e:
                logging.error(
                    f"Failed to execute preprocess function in {template_name}.py: {e}"
                )
    formatted_template = template.format(**kwargs)
    return formatted_template, subject


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


def broadcast_emails(
    template_name: str, email_task_lock: Lock, mongodb_search_condition: dict = {}
):
    # Iter over all users and send them an email
    try:
        cursor = users_collection.find(
            mongodb_search_condition, InternalConfig.internal_columns
        )
        for user in cursor:
            try:
                send_email(template_name, user["email"], **user)
            except Exception as e:
                logging.error(
                    f"Failed to send email to {user['email']} with Template {template_name}: {e}"
                )
    except Exception as e:
        raise e
    finally:
        email_task_lock.release_lock()
