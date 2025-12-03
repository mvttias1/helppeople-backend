# help_app/email_utils.py
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


import os
from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail import send_mail

# -------------------------------------------------------------------
# 1) Correos de notificación de DONACIONES (SendGrid / API externa)
# -------------------------------------------------------------------

# A quiénes se les avisa cuando entra una nueva donación
NOTIFICACIONES_DONACIONES = [
    "matiasdonoso135@gmail.com",   # puedes agregar más correos si quieres
]


def enviar_correo_notificacion_donacion(donacion):
    """
    Envía un correo de notificación cuando se registra una donación.
    Usa SendGrid como API externa.
    """
    # Intentamos leer la API key desde settings o variable de entorno
    api_key = getattr(settings, "SENDGRID_API_KEY", None) or os.environ.get("SENDGRID_API_KEY")

    if not api_key:
        print("⚠️ No se encontró SENDGRID_API_KEY, no se envió correo.")
        return False

    # Asunto del correo
    subject = f"Nueva donación en Help People - {donacion.nombre} {donacion.apellido}"

    # Contenido HTML del correo
    html_content = f"""
    <h2>Nueva donación registrada</h2>
    <p><strong>Nombre:</strong> {donacion.nombre} {donacion.apellido}</p>
    <p><strong>RUT:</strong> {donacion.rut}</p>
    <p><strong>Documento:</strong> {donacion.documento}</p>
    <p><strong>Correo:</strong> {donacion.correo}</p>
    <p><strong>Teléfono:</strong> {donacion.telefono}</p>
    <p><strong>Certificado:</strong> {donacion.certificado}</p>
    <hr>
    <p>Este correo fue generado automáticamente por el sistema Help People.</p>
    """

    # Remitente: usa algo coherente con tu proyecto / cuenta SendGrid
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "matiasdonoso135@gmail.com")

    message = Mail(
        from_email=from_email,
        to_emails=NOTIFICACIONES_DONACIONES,
        subject=subject,
        html_content=html_content,
    )

    try:
        sg = SendGridAPIClient(api_key)
        response = sg.send(message)
        print("✅ Correo de donación enviado. Status:", response.status_code)
        return True
    except Exception as e:
        print("❌ Error enviando correo de donación:", e)
        return False


# -------------------------------------------------------------------
# 2) Correo simple (usa el backend de Django, no la API externa)
# -------------------------------------------------------------------
def enviar_correo(destinatario, asunto, mensaje):
    """
    Envía un correo simple usando el backend de correo de Django.
    (Sirve si en el futuro configuras SMTP directo).
    """
    try:
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@helppeople.cl"),
            recipient_list=[destinatario],
            fail_silently=False,
        )
        print("✅ Correo simple enviado correctamente")
        return True
    except Exception as e:
        print("❌ Error enviando correo:", e)
        return False
