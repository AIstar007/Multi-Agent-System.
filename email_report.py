import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 465))
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

REPORT_FILES = [
    ("results/eval_report.pdf", "application/pdf"),
    ("results/eval_report.csv", "text/csv")
]

msg = EmailMessage()
msg['Subject'] = "📊 Multi-Agent System Evaluation Report"
msg['From'] = EMAIL_SENDER
msg['To'] = EMAIL_RECEIVER
msg.set_content(
    "Hello,\n\nAttached are the latest evaluation reports (PDF and CSV) from your Multi-Agent AI System.\n\nBest,\nMulti-Agent Bot 🤖"
)

for file_path, mime_type in REPORT_FILES:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            file_data = f.read()
            file_name = os.path.basename(file_path)
            maintype, subtype = mime_type.split("/")
            msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)
    else:
        print(f"⚠️ Warning: {file_path} not found. Skipping attachment.")

try:
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)
        print("✅ Email sent successfully.")
except Exception as e:
    print(f"❌ Email sending failed: {e}")