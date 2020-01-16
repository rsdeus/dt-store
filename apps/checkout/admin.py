from django.contrib import admin

from .models import CartItem, Order, OrderItem, PaymentMethods


admin.site.register([CartItem, Order, OrderItem, PaymentMethods])
