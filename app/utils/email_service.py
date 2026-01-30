import smtplib
from email.mime.text import MIMEText

SMTP_EMAIL = "autispectra@gmail.com"
SMTP_PASSWORD = "vctbsvcnuryrkozu"

def send_verification_email(to_email: str, code: str):
    subject = "Your Password Reset Code"
    body = f"Your verification code is: {code}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SMTP_EMAIL, SMTP_PASSWORD)
    server.sendmail(SMTP_EMAIL, to_email, msg.as_string())
    server.quit()
