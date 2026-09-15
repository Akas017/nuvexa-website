import os
import smtplib
from pathlib import Path
from email.message import EmailMessage

from dotenv import load_dotenv


# Load .env from the backend directory
BASE_DIR = Path(__file__).resolve().parents[2]
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_TO = os.getenv("MAIL_TO")


def send_contact_notification(
    name: str,
    email: str,
    project_type: str,
    message: str,
) -> None:
    if not MAIL_USERNAME or not MAIL_PASSWORD or not MAIL_TO:
        raise RuntimeError(
            "MAIL_USERNAME, MAIL_PASSWORD and MAIL_TO must be configured."
        )

    email_message = EmailMessage()

    email_message["Subject"] = f"New NUVEXA Project Enquiry — {project_type}"
    email_message["From"] = MAIL_USERNAME
    email_message["To"] = MAIL_TO
    email_message["Reply-To"] = email

    email_message.set_content(
        f"""
New project enquiry received through NUVEXA website.

Name:
{name}

Email:
{email}

Project Type:
{project_type}

Message:
{message}

----------------------------------------
NUVEXA
Digital Systems Studio
"""
    )

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as smtp:
        smtp.starttls()
        smtp.login(MAIL_USERNAME, MAIL_PASSWORD)
        smtp.send_message(email_message)