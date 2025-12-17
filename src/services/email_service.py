import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


class EmailService:
    def __init__(self):
        # 🔐 НАСТРОЙКИ ПОЧТЫ
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587

        self.sender_email = "cubiks572@gmail.com"
        self.sender_password = "qwuv geln rrgs wfdf"
        self.receiver_email = "gnezdilovzena40@gmail.com"

    def send_alert(self, title: str, message: str):
        try:
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = self.receiver_email
            msg["Subject"] = title

            body = f"""
⚠️ УВЕДОМЛЕНИЕ УМНОГО ДОМА

{message}

Дата и время:
{datetime.now().strftime("%d.%m.%Y %H:%M:%S")}
            """

            msg.attach(MIMEText(body, "plain", "utf-8"))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()

            print("📧 Email отправлен")

            return True

        except Exception as e:
            print(f"❌ Ошибка отправки email: {e}")
            return False