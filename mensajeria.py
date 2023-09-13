from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from smtplib import SMTP
from validate_email import validate_email
from os import environ

def cambiarPassword(destinatario):
    existeEmail = validate_email(destinatario)

    if not existeEmail:
        return
    texto = """  
    Te informamos que tu contraseña para Technology se ha modificado recientemente. Si has sido tú, no tienes que hacer nada más. Si no reconoces este cambio, por favor, verifica tu actividad de inicio de sesión y contacta con nosotros si detectas algo sospechoso.
    """
     # Ruta de la imagen que deseas adjuntar
    imagen_path = 'imagenes/Gracias.jpg'

    emailEmisor = environ.get('EMAIL_EMISOR')
    passwordEmisor = environ.get('PASSWORD_EMISOR')

    cuerpo = MIMEText(texto, 'html')
    correo = MIMEMultipart()
    correo['Subject'] = 'Cambio de contraseña'
    correo['To'] = destinatario
    correo.attach(cuerpo)

     # Adjunta la imagen al correo
    with open(imagen_path, 'rb') as imagen_file:
        imagen = MIMEImage(imagen_file.read())
        correo.attach(imagen)

    emisor = SMTP('smtp.gmail.com',587)
    emisor.starttls()
    emisor.login(emailEmisor, passwordEmisor)
    emisor.sendmail(from_addr="Technology <" + emailEmisor + ">", to_addrs=destinatario, msg=correo.as_string())
    emisor.quit()
