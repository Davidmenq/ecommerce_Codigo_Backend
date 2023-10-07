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
    # with open(imagen_path, 'rb') as imagen_file:
    #     imagen = MIMEImage(imagen_file.read())
    #     correo.attach(imagen)

    emisor = SMTP('smtp.gmail.com',587)
    emisor.starttls()
    emisor.login(emailEmisor, passwordEmisor)
    emisor.sendmail(from_addr="Technology <" + emailEmisor + ">", to_addrs=destinatario, msg=correo.as_string())
    emisor.quit()

def enviarMensaje(mensaje):
    nombre=mensaje.get('nombre')
    apellido=mensaje.get('apellido')
    empresa=mensaje.get('empresa')
    email=mensaje.get('email')
    localidad=mensaje.get('localidad')
    telefono=mensaje.get('telefono')
    contenido=mensaje.get('mensaje')
    politica=mensaje.get('politicas')

    texto = f"""  
    {nombre} / {apellido} / 
    {empresa} / {email} / {localidad} / {telefono} / 
    {contenido} / Estoy de acuerdo con la politica: {politica}
    """

    emailEmisor = environ.get('EMAIL_EMISOR')
    passwordEmisor = environ.get('PASSWORD_EMISOR')

    cuerpo = MIMEText(texto, 'html')
    correo = MIMEMultipart()
    correo['Subject'] = f'Mensaje enviado desde E-COMMERCE TECHNOLOGY - {nombre} {apellido} '
    correo['To'] = environ.get('EMAIL_CONTACTO')
    correo.attach(cuerpo)

    emisor = SMTP('smtp.gmail.com',587)
    emisor.starttls()
    emisor.login(emailEmisor, passwordEmisor)
    emisor.sendmail(from_addr="Technology <" + emailEmisor + ">", to_addrs=environ.get('EMAIL_CONTACTO'), msg=correo.as_string())
    emisor.quit()


def enviarRutaCambiarContrasena(destinatario):
    enlace = "https://ecommerce-api-backend-nlld.onrender.com/cambiar-contrasena"  # URL del enlace
    texto = f"""
    Usa este <a href="{enlace}">enlace</a> para cambiar tu contraseña. Si no quieres cambiar tu contraseña, ignora este mensaje.
    """
    emailEmisor = environ.get('EMAIL_EMISOR')
    passwordEmisor = environ.get('PASSWORD_EMISOR')

    cuerpo = MIMEText(texto, 'html')
    correo = MIMEMultipart()
    correo['Subject'] = 'Recuperar contraseña'
    correo['To'] = destinatario
    correo.attach(cuerpo)

    emisor = SMTP('smtp.gmail.com',587)
    emisor.starttls()
    emisor.login(emailEmisor, passwordEmisor)
    emisor.sendmail(from_addr="Technology <" + emailEmisor + ">", to_addrs=destinatario, msg=correo.as_string())
    emisor.quit()
