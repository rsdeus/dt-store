
# coding=utf-8

from django.contrib.auth.backends import ModelBackend as BaseModelBackend

from django.contrib.auth import get_user_model

class ModelBackend(BaseModelBackend):

    def authenticate(self, email=None, password=None):
        if email:
            try:
                user = get_user_model(email=email)
                if user.check_password(password):
                    return user
            except user.DoesNotExist:
                pass
