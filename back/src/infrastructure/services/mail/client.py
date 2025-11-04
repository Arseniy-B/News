import smtplib
from email.message import EmailMessage
from src.config import config


class MailSender:
    def __init__(self):
        msg = EmailMessage()
        msg["From"] = config.mail.MAIL_ADDRESS
        msg.set_content("Well come")
        self.msg = msg

    def send_message(self, recipient_address: str):
        self.msg["To"] = recipient_address
        with smtplib.SMTP_SSL(config.mail.SMTP_SERVER, 465) as smtp:
            smtp.login(config.mail.MAIL_ADDRESS, config.mail.MAIL_PASSWORD)
            smtp.send_message(self.msg)
