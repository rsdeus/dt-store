# coding=utf-8
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import View, TemplateView
from django.contrib.auth.views import LogoutView as BaseLogoutView

from django.http import JsonResponse

from .forms import ContactForm

class IndexView(TemplateView):
    pass


def contact(request):
    form = ContactForm()
    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)


def contact_submit(request):
    if request.method == "POST" and request.is_ajax():
        form = ContactForm(request.POST)
        if form.is_valid():
            form.send_mail()
            return JsonResponse({"success": True, "message": "Email Enviado"}, status=200)
    else:
        return JsonResponse({"success": False, "message": "Email Não Enviado"}, status=400)
