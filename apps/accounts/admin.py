# coding=utf-8

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminForm
from django.contrib.auth import get_user_model
from apps.accounts.models import UserAddress


User = get_user_model()


class UserAdmin(BaseUserAdmin):

    add_form = UserAdminCreationForm
    add_fieldsets = (
        (None, {
            'fields':
                ['email', 'first_name', 'password1', 'password2', 'address']
        }),
    )
    form = UserAdminForm
    fieldsets = [
        (None, {
            'fields': ['email', 'first_name']
        }),
        ('Informações Básicas', {
            'fields': ['last_name', 'last_login']
        }),
        ('Endereço de Entrega', {
            'fields': ['shipping_address']
        }),
        ('Endereço de Cobrança', {
            'fields': ['billing_address']
        }),
        ('Contatos', {
            'fields': ['phone']
        }),
        ('Permissões', {
            'fields': ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']
        }),
    ]
    ordering = ['email']
    list_display = ['email', 'first_name', 'last_name', 'phone', 'is_active', 'is_staff', 'date_joined', 'shipping_address', 'billing_address']


admin.site.register(User, UserAdmin)
admin.site.register(UserAddress)
