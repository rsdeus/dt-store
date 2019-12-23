# coding=utf-8

from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.contrib.auth import get_user_model

from core.utils import *


class UserAdminCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            dt_sendmail(self, 'register', 'Registro no site DT-Store', 'Bem vindo ao site DT-Store', self.cleaned_data["email"])
        return user


class UserAdminForm(forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ['email', 'first_name', 'last_name', 'is_active', 'is_staff']
