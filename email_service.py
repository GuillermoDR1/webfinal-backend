import smtplib
from email.message import EmailMessage
import os

def enviar_correo_contacto(destinatario, asunto, cuerpo):
    # Leemos las variables exactas que pusiste en tu .env
    remitente = os.getenv("MAIL_USER") 
    password = os.getenv("MAIL_PASSWORD")
    servidor = os.getenv("MAIL_SERVER")
    puerto = int(os.getenv("MAIL_PORT"))

    msg = EmailMessage()
    msg.set_content(cuerpo)
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = destinatario

    try:
        print("Intentando conectar a Gmail...")
        # Le agregamos un límite de 5 segundos para que no congele la página
        server = smtplib.SMTP(servidor, puerto, timeout=5)
        server.starttls() 
        server.login(remitente, password)
        
        print("Enviando mensaje...")
        server.send_message(msg)
        server.quit()
        
        print("Correo enviado exitosamente a:", destinatario)
        return True
    except Exception as e:
        print(f"Error al enviar correo (posible bloqueo de puerto o timeout): {e}")
        return False