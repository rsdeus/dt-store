# coding=utf-8
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import CreateView, TemplateView, UpdateView, FormView
from django.urls import reverse_lazy

from django.contrib.auth import get_user_model
from .forms import UserAdminCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(LoginRequiredMixin, TemplateView):
    pass


class RegisterView(CreateView):

    model = get_user_model()
    form_class = UserAdminCreationForm
    success_url = reverse_lazy('accounts:index')


class UpdateUserView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = 'accounts/update_user.html'
    fields = ['email', 'first_name', 'last_name', 'phone']
    success_url = reverse_lazy('accounts:index')

    def get_object(self):
        return self.request.user


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'accounts/update_password.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('accounts:index')

    def get_form_kwargs(self):
        kwargs = super(UpdatePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(UpdatePasswordView, self).form_valid(form)
