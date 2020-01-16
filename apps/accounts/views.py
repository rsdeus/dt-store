# coding=utf-8
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse, request
from django.shortcuts import render, redirect
from django.contrib import messages, sessions
from django.views.generic import CreateView, TemplateView, UpdateView, FormView, RedirectView
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import UserAddress, User
from apps.checkout.models import CartItem, Order

import logging


class IndexView(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        session_key = self.request.session.session_key
        context['go_to_cart'] = False
        context['go_to_order'] = False
        if self.request.user.is_authenticated:
            if session_key and CartItem.objects.filter(cart_key=session_key).exists():
                context['go_to_cart'] = True
            if Order.objects.filter(user=self.request.user, payment_status=0).exists():
                context['go_to_order'] = True

        return context

        
class RegisterView(CreateView):

    model = get_user_model()
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('accounts:index')

    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, 'Registro criado com Sucesso')
        except:
            messages.error(self.request, 'Falha ao Criar Registro')

        return super().form_valid(form)
    

class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'accounts/update_user.html'
    fields = ['email', 'first_name', 'last_name', 'phone']
    success_url = reverse_lazy('accounts:index')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, 'Dados Alterados com Sucesso')
        except:
            messages.error(self.request, 'Falha ao Salvar Dados')

        return super().form_valid(form)


class UpdateUserAddressView(LoginRequiredMixin, UpdateView):
    model = UserAddress
    template_name = 'accounts/update_user_address.html'
    fields = ['locality', 'street_number', 'complement', 'neighborhood', 'postal_code', 'city', 'state', 'country']
    success_url = reverse_lazy('accounts:index')

    def get_object(self):
        return self.request.user.shipping_address

    def form_valid(self, form):
        user = User.objects.get(pk=self.request.user.pk)
        if user:
            user.shipping_address = self.object

        if self.object.is_billing_address:
            user.billing_address = self.object

        try:
            user.save()
            messages.success(self.request, 'Endereço Alterado com Sucesso')
        except:
            messages.error(self.request, 'Falha ao Salvar o Endereço')

        form.save()
        return super().form_valid(form)


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'accounts/update_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('accounts:index')

    def get_form_kwargs(self):
        kwargs = super(UpdatePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        try:
            form.save()
            messages.success(self.request, 'Senha Alterada com Sucesso')
        except:
            messages.error(self.request, 'Falha ao Alterar a Senha')

        return super(UpdatePasswordView, self).form_valid(form)
