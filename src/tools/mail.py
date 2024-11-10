import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .conf import EmailConfig
from api.helpers.log import logger
from threading import Lock
from tools import users_collection, InternalConfig
import importlib
import re
import threading
import queue

smtp = smtplib.SMTP_SSL(EmailConfig.smtp_host, EmailConfig.smtp_port)
email_queue = queue.Queue()


def queue_email(template_name: str, to: str, **kwargs):
    email_queue.put_nowait(lambda: send_email(template_name, to, **kwargs))


def fill_placeholders(template: str, data: dict) -> str:
    pattern = re.compile(r"\{\{\s*(\w+)\s*\}\}")
    result = pattern.sub(
        lambda match: str(data.get(match.group(1), match.group(0))), template
    )
    return result


def load_template(template_name: str, **kwargs) -> str:
    with open(f"/src/app/config/email/{template_name}.html", "r") as file:
        template = file.read()
    if template.find("<title>") == -1:
        raise ValueError("Template does not contain a title tag")
    subject = template[template.find("<title>") + 7 : template.find("</title>")]
    # Try to find template_name + ".py" and execute the function "preprocess"
    try:
        module = importlib.import_module(f"config.email.{template_name}")
    except ModuleNotFoundError:
        pass
    else:
        logger.debug(f"Found preprocess function in {template_name}.py")
        if hasattr(module, "preprocess"):
            logger.debug(f"Executing preprocess function in {template_name}.py")
            try:
                kwargs = module.preprocess(kwargs)
            except Exception as e:
                logger.error(
                    f"Failed to execute preprocess function in {template_name}.py: {e}"
                )
    formatted_template = fill_placeholders(template, kwargs)
    subject = fill_placeholders(subject, kwargs)
    return formatted_template, subject


def send_email(template_name: str, to: str, **kwargs):
    html_content, subject = load_template(template_name, **kwargs)

    msg = MIMEMultipart()
    msg["From"] = EmailConfig.sender_email
    msg["To"] = to
    msg["Subject"] = subject

    # Attach HTML content
    msg.attach(MIMEText(html_content, "html"))

    logger.debug(f"Sending email to {to} with subject: {subject}")
    # Send email
    smtp.login(EmailConfig.login_usr, EmailConfig.login_pwd)
    smtp.send_message(msg)

    logger.info(f"Email sent to {to} with subject: {subject}")


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
                logger.error(
                    f"Failed to send email to {user['email']} with Template {template_name}: {e}"
                )
    except Exception as e:
        raise e
    finally:
        email_task_lock.release_lock()


def email_worker():
    logger.info("\u001b[32m- E-Mail Worker started\u001b[0m")
    while True:
        email_task = email_queue.get()
        try:
            email_task()
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
        email_queue.task_done()


threading.Thread(target=email_worker, daemon=True).start()
