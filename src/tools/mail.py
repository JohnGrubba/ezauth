import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from . import config

smtp_host = config["email"]["smtp_host"]
smtp_port = config["email"]["smtp_port"]
username = config["email"]["login_usr"]
password = config["email"]["login_pwd"]
sender_email = config["email"]["sender_email"]


def load_template(template_name: str, **kwargs) -> str:
    with open(f"/src/app/config/email/{template_name}.html", "r") as file:
        template = file.read()
    subject = template[template.find("<title>") + 7 : template.find("</title>")]
    return template.format(**kwargs), subject


def send_email(template_name: str, to: str, **kwargs):
    html_content, subject = load_template(template_name, **kwargs)

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to
    msg["Subject"] = subject

    # Attach HTML content
    msg.attach(MIMEText(html_content, "html"))

    # Send email
    with smtplib.SMTP_SSL(smtp_host, smtp_port) as server:
        server.login(username, password)
        server.send_message(msg)

    print("Email sent successfully!")
