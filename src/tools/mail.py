import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from tools import config

smtp_host = config["email"]["smtp_host"]
smtp_port = config["email"]["smtp_port"]
username = config["email"]["smtp_port"]
password = config["email"]["smtp_port"]

# Email details
from_addr = "your_email@example.com"
to_addr = "recipient_email@example.com"
subject = "HTML Email Test"
html_content = """
<html>
  <head></head>
  <body>
    <p>Hello,<br>
       How are you?<br>
       Here is the <a href="http://www.example.com">link</a> you wanted.
    </p>
  </body>
</html>
"""

# Create message
msg = MIMEMultipart()
msg["From"] = from_addr
msg["To"] = to_addr
msg["Subject"] = subject

# Attach HTML content
msg.attach(MIMEText(html_content, "html"))

# Send email
with smtplib.SMTP(smtp_host, smtp_port) as server:
    server.starttls()  # Secure the connection
    server.login(username, password)
    server.send_message(msg)

print("Email sent successfully!")
