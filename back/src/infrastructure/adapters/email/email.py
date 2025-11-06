from src.infrastructure.services.email.client import EmailSender
from src.domain.port.email import EmailPort, Otp
from src.config import config


class EmailAdapter(EmailPort):
    async def send_otp(self, email: str, otp: Otp):
        msg = EmailSender()
        msg.send_message(email, config.email.get_otp_content(otp))

    async def send_welcome(self, email: str):
        msg = EmailSender()
        msg.send_message(email, config.email.get_welcome_content())

