"""dtstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from core import views

urlpatterns = [
    path('', views.IndexView.as_view(template_name='index.html'), name='index'),
    path('contato/', views.contact, name='contact'),
    path('contato/submit', views.contact_submit, name='contact_submit'),
    path('entrar/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('recuperar-senha/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('confimacao-senha/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('recuperar-senha/enviada/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('recuperar-senha/concluida/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('sair/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('catalogo/', include('apps.catalog.urls', namespace='catalog')),
    path('conta/', include('apps.accounts.urls', namespace='accounts')),
    path('checkout/', include('apps.checkout.urls', namespace='checkout')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
