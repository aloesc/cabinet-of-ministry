import aiosmtplib
from email.message import EmailMessage
import os

async def send_email(to: str, subject: str, body: str):
    message = EmailMessage()
    message["From"] = "support@egd.ru"
    message["To"] = to
    message["Subject"] = subject
    message.set_content(body)

    await aiosmtplib.send(
        message,
        hostname=os.getenv("SMTP_HOST", "sandbox.smtp.mailtrap.io"),
        port=int(os.getenv("SMTP_PORT", 2525)),
        username=os.getenv("SMTP_USER", "17d27c70398559"),
        password=os.getenv("SMTP_PASS", "cab3a0e7b8dd08"),
    )
