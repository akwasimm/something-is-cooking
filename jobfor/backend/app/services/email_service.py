import logging
from email.message import EmailMessage
import aiosmtplib

from app.core.config import settings

logger = logging.getLogger(__name__)

async def send_job_alert_email(to_email: str, job_count: int, alert_name: str, link: str):
    """
    Sends an async HTML email utilizing native standard email loops and aiosmtplib structures mapping limits efficiently.
    """
    if not settings.SMTP_HOST or not settings.SMTP_USER:
        logger.warning("SMTP Config missing. Skipping email dispatch mapping.")
        return

    msg = EmailMessage()
    msg["From"] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = f"JobFor | {job_count} New Matches for '{alert_name}'"

    host_url = "http://localhost:5173"
    full_link = f"{host_url}{link}"

    html_content = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.6;">
        <h2 style="color: #4F46E5;">New Opportunities Found!</h2>
        <p>We tracked <strong>{job_count}</strong> new opportunities matching your <em>{alert_name}</em> parameters.</p>
        <p style="margin-top: 20px;">
          <a href="{full_link}" style="display:inline-block;padding:12px 24px;background:#6366F1;color:#fff;text-decoration:none;border-radius:6px;font-weight:bold;">
            View Jobs Now
          </a>
        </p>
        <p style="margin-top: 30px; font-size: 12px; color: #888;">
          You are receiving this because you subscribed to '{alert_name}' on JobFor.
        </p>
      </body>
    </html>
    """
    msg.add_alternative(html_content, subtype="html")

    try:
        await aiosmtplib.send(
            msg,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=True if settings.SMTP_PORT == 465 else False,
            start_tls=True if settings.SMTP_PORT == 587 else False,
        )
        logger.info(f"Successfully dispatched alert email to {to_email}")
    except Exception as e:
        logger.error(f"Failed to send isolated email mapping to {to_email}: {str(e)}")
