import os
import smtplib
from email.message import EmailMessage

def enviar_correo(destinatario, asunto, mensaje):
    SMTP_HOST = "smtp.sendgrid.net"
    SMTP_PORT = 587
    SMTP_USER = "apikey"
    SMTP_PASSWORD = os.environ.get("SENDGRID_API_KEY")

    if not SMTP_PASSWORD:
        print("❌ SENDGRID_API_KEY no configurada")
        return False

    msg = EmailMessage()
    msg["From"] = "no-reply@helppeople.local"
    msg["To"] = destinatario
    msg["Subject"] = asunto
    msg.set_content(mensaje)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        print("✅ Correo enviado correctamente")
        return True
    except Exception as e:
        print("❌ Error enviando correo:", e)
        return False
