import os

from prefect_email import EmailServerCredentials

try:
    EmailServerCredentials.load("email-notify")
except ValueError:
    credentials = EmailServerCredentials(
        username=os.getenv("ADMIN_EMAIL"),
        password=os.getenv("ADMIN_PASSCODE"),
    )
    credentials.save(name="email-notify")
