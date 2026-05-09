import asyncio
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib

from config import settings

logger = logging.getLogger(__name__)


async def _send_email(to: str, subject: str, html_body: str) -> None:
    if not settings.email_enabled:
        return

    message = MIMEMultipart("alternative")
    message["From"] = settings.email_from or settings.email_username
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(html_body, "html", "utf-8"))

    try:
        await aiosmtplib.send(
            message,
            hostname=settings.email_host,
            port=settings.email_port,
            username=settings.email_username,
            password=settings.email_password,
            start_tls=True,
        )
        logger.info("Email sent to %s", to)
    except Exception:
        logger.exception("Failed to send email to %s", to)


def send_welcome_email(to: str, username: str) -> None:
    """Deprecated sync wrapper — use send_welcome_email_async instead."""
    pass


async def send_welcome_email_async(to: str, username: str) -> None:
    """Fire-and-forget welcome email after user registration."""
    if not to or not settings.email_enabled:
        return

    subject = "Chào mừng đến với Give & Take / Welcome to Give & Take"
    html_body = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: auto;">

        <!-- Vietnamese -->
        <div style="border-left: 4px solid #e74c3c; padding-left: 16px; margin-bottom: 32px;">
          <h2 style="color: #e74c3c;">Chào mừng đến với Give & Take 🎁</h2>
          <p>Xin chào <strong>{username}</strong>,</p>
          <p>
            Tài khoản của bạn đã được tạo thành công trên nền tảng
            <strong>Give & Take</strong> — nơi kết nối những tấm lòng nhân ái với
            những hoàn cảnh khó khăn.
          </p>
          <p>Bạn có thể đăng nhập và bắt đầu hành trình thiện nguyện của mình ngay hôm nay.</p>
          <p style="margin-top: 16px;">Trân trọng,<br/>Đội ngũ Give & Take</p>
        </div>

        <hr style="border: none; border-top: 1px solid #ddd; margin: 0 0 32px;"/>

        <!-- English -->
        <div style="border-left: 4px solid #e74c3c; padding-left: 16px;">
          <h2 style="color: #e74c3c;">Welcome to Give & Take 🎁</h2>
          <p>Hello <strong>{username}</strong>,</p>
          <p>
            Your account has been successfully created on <strong>Give & Take</strong>
            — a platform that connects generous hearts with people in need.
          </p>
          <p>You can log in and start your charitable journey today.</p>
          <p style="margin-top: 16px;">Best regards,<br/>The Give & Take Team</p>
        </div>

      </body>
    </html>
    """

    await _send_email(to, subject, html_body)
    logger.info("Welcome email sent to %s", to)
