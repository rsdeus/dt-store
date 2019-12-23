from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages


def dt_sendmail(self, message_type, subject, message, email):

    if message_type is 'register':
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        # return_message = 'E-mail de registo enviado com sucesso' :TODO implementar logging e aviso de sucesso ou erro
    elif message_type is 'recover_password':
        pass

    #return messages.info(self.request, return_message)
