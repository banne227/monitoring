import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load the .env
load_dotenv()

def send_email(annonce):
    password = os.getenv("EMAIL_APP_PASSWORD")
    sender_email = os.getenv("EMAIL_ADDRESS")
    receiver_email = os.getenv("EMAIL_TO")

    body = f"Nouvelle annonce trouvée :\n\nLien : {annonce['link']}\nPrix : {annonce['price']}\nVille : {annonce['city']}"
    msg = MIMEText(body)
    msg['Subject'] = "Nouvelle annonce PAP"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    print(f"Sending email to {receiver_email} for {annonce['ID']}...")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Email sent")
