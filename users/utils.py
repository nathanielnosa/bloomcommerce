from django.core.mail import send_mail
from django.conf import settings

def emailSender(fullname,email):
    subject = "Welcome To Bloom App."
    body = f'''
            Hello {fullname}, you have successfully register,
            kindly follow us on our news update.
            '''
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )