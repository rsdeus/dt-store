# coding=utf-8

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from apps.address.models import Address

from django.conf import settings

class UserManager(BaseUserManager):

    def create_user(self, email, first_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserAddress(Address):
    pass


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('E-mail', unique=True)
    first_name = models.CharField('Nome', max_length=100, blank=True)
    last_name = models.CharField('Sobrenome', max_length=100, blank=True)
    # profile = model.CharField('Perfil') :TODO estudar sobre permissões e criar perfis, customer e vendor
    is_staff = models.BooleanField('Equipe', default=False)
    is_active = models.BooleanField('Ativo', default=True)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)
    phone = models.CharField('Telefone', max_length=12, blank=True)
    shipping_address = models.ForeignKey('UserAddress', related_name='shipping_address', on_delete=models.CASCADE, verbose_name='Endereço de Entrega', blank=True, null=True)
    billing_address = models.ForeignKey('UserAddress', related_name='billing_address', on_delete=models.CASCADE, verbose_name='Endereço de Cobrança', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    objects = UserManager()

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.first_name or self.username
