# coding=utf-8

from django.shortcuts import get_object_or_404, redirect
from django.views.generic import RedirectView, TemplateView, ListView, DetailView, View
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
import json
from django.views.decorators.vary import vary_on_headers

from apps.catalog.models import Product

from apps.checkout.forms import CartItemFormSet, ShippingMethodsFormSet, PickupDayShippingMethodFormSet, DeliveryByCorreiosShippingMethodFormSet, UserShippingAddressFormSet, PaymentMethodFormSet

from .models import CartItem, Order, ShippingMethods, PaymentMethods

from pagseguro import PagSeguro

import logging

logger = logging.getLogger()


class CreateCartItemView(View):

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        if self.request.session.session_key is None:
            self.request.session.save()
        try:
            cart_item, created = CartItem.objects.add_item(
                self.request.session.session_key, product
            )
        except ValidationError as e:
            messages.info(self.request, e.message)
            return reverse('catalog:product_list')
        else:
            if created:
                message = 'Produto adicionado com sucesso'
            else:
                message = 'Produto atualizado com sucesso'
            if request.is_ajax():
                return HttpResponse(
                    json.dumps({'message': message}), content_type='application/json'
                )
            else:
                messages.info(self.request, 'Produto atualizado com sucesso')
        return redirect('checkout:cart-item')


class CartItemView(TemplateView):

    template_name = 'checkout/cart.html'

    def get_cart_item_formset(self, post=True):
        session_key = self.request.session.session_key
        if session_key:
            if post:
                messages.info(self.request, self.request.POST)
                cart_item_formset = CartItemFormSet(
                    queryset=CartItem.objects.filter(cart_key=session_key),
                    prefix='cart_item',
                    data=self.request.POST or None
                )
            else:
                cart_item_formset = CartItemFormSet(
                    queryset=CartItem.objects.filter(cart_key=session_key),
                    prefix='cart_item'
                )
        else:
            cart_item_formset = CartItemFormSet(queryset=CartItem.objects.none(), prefix='cart_item')

        return cart_item_formset

    def get_shipping_formset(self, post=True):
        if post:
            shipping_method_formset = ShippingMethodsFormSet(
                prefix='shipping_methods',
                data=self.request.POST or None
            )
        else:
            shipping_method_formset = ShippingMethodsFormSet(
                prefix='shipping_methods'
            )
        return shipping_method_formset

    def get_pickup_day_shipping_method_formset(self, post=True):
        if post:
            pickup_day_shipping_method_formset = PickupDayShippingMethodFormSet(
                prefix='pickup_day_shipping_method',
                data=self.request.POST or None
            )
        else:
            pickup_day_shipping_method_formset = PickupDayShippingMethodFormSet(
                prefix='pickup_day_shipping_method'
            )
        return pickup_day_shipping_method_formset

    def get_delivery_by_correios_shipping_method_formset(self, post=True):
        if post:
            delivery_by_correios_shipping_method_formset = DeliveryByCorreiosShippingMethodFormSet(
                prefix='delivery_by_correios_shipping_method',
                data=self.request.POST or None
            )
        else:
            delivery_by_correios_shipping_method_formset = DeliveryByCorreiosShippingMethodFormSet(
                prefix='delivery_by_correios_shipping_method'
            )
        return delivery_by_correios_shipping_method_formset

    def get_user_shipping_address(self, post=True):
        if post:
            user_shipping_address_formset = UserShippingAddressFormSet(
                prefix='user_shipping_address',
                data=self.request.POST or None
            )
        else:
            user_shipping_address_formset = UserShippingAddressFormSet(
                prefix='user_shipping_address',
            )
        return user_shipping_address_formset

    def get_context_data(self, **kwargs):
        context = super(CartItemView, self).get_context_data(**kwargs)
        session_key = self.request.session.session_key
        if not CartItem.objects.filter(cart_key=session_key).exists():
            context['empty_cart_item'] = True
        context['cart_item_formset'] = self.get_cart_item_formset(post=False)

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        session_key = self.request.session.session_key
        cart_item_formset = CartItemFormSet(
            queryset=CartItem.objects.filter(cart_key=session_key),
            prefix='cart_item',
            data=self.request.POST
        )
        if cart_item_formset.is_valid():
            cart_item_formset.save()
            logger.info(self.request.POST)
            message = "Cesta Atualizada"
        else:
            message = "Falha ao atualizar a Cesta"
            logger.info(self.request.POST)
            
        logger.info(message)
        
        if self.request.is_ajax():
            return JsonResponse({"message": message})
        else:
            message = "Falha na requisição Ajax"
            context['cart_item_formset'] = cart_item_formset
            logger.info(message)
            logger.info(self.request.POST)
            return self.render_to_response(context)


class CreateOrderView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        session_key = self.request.session.session_key
        if session_key and CartItem.objects.filter(cart_key=session_key).exists():
            cart_items = CartItem.objects.filter(cart_key=session_key)
            order = Order.objects.create_order(
                user=self.request.user, cart_items=cart_items, session_key=session_key
            )
            cart_items.delete()
        else:
            super(CreateOrderView, self).get_redirect_url(*args, **kwargs)
            messages.info(self.request, 'Não há itens no carrinho de compras')
            return reverse('checkout:cart-item')

        return reverse('checkout:payment', kwargs={'pk': order.pk})


class OrderListView(LoginRequiredMixin, ListView):

    template_name = 'checkout/order_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetailView(LoginRequiredMixin, DetailView):

    template_name = 'checkout/order_detail.html'

    def get_queryset(self, *args, **kwargs):
        return Order.objects.filter(user=self.request.user, pk=self.kwargs['pk'])


class PaymentView(LoginRequiredMixin, TemplateView):

    template_name = 'checkout/checkout.html'

    def get_payment_methods_formset(self, post=False):
        if post:
            payment_methods_formset = PaymentMethodFormSet(
                prefix='payment_methods',
                data=self.request.POST or None
            )
        else:
            payment_methods_formset = PaymentMethodFormSet(
                prefix='payment_methods',
            )
        return payment_methods_formset

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)
        order = Order.objects.get(pk=self.kwargs['pk'])
        context['order'] = order
        payment_methods_formset = self.get_payment_methods_formset()
        if order.shipping_method == 'store_pickup':
            for form in payment_methods_formset:
                form.fields['payment_option'].choices = PaymentMethods.PAYMENT_OPTION_CHOICES_DELIVERY
                context['payment_methods_formset'] = payment_methods_formset
        else:
            context['payment_methods_formset'] = payment_methods_formset
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        order = Order.objects.get(pk=self.kwargs['pk'])
        context['order'] = order
        payment_methods_formset = self.get_payment_methods_formset(post=True)
        if order.shipping_method == 'store_pickup':
            for form in payment_methods_formset:
                form.fields['payment_option'].choices = PaymentMethods.PAYMENT_OPTION_CHOICES_DELIVERY
                context['payment_methods_formset'] = payment_methods_formset
        else:
            context['payment_methods_formset'] = payment_methods_formset

        if request.POST.get('PaymentMethod') == 'get_payment_method':
            payment_method = payment_methods_formset.cleaned_data[0]['payment_option']
            if payment_method == 'payment_on_delivery_cash':
                messages.info(request, payment_method)
                reverse('checkout:payment-on-delivery', kwargs={'pk': order.pk})
        return self.render_to_response(context)


class PagSeguroView(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(
            Order.objects.filter(user=self.request.user, pk=order_pk)
        )
        payment = PaymentMethods.objects.create(order=order)
        pg = payment.pagseguro()
        pg.redirect_url = self.request.build_absolute_uri(
            reverse('checkout:order-detail', args=[order.pk])
        )
        pg.notification_url = self.request.build_absolute_uri(
            reverse('checkout:pagseguro_notification')
        )
        response = pg.checkout()
        return response.payment_url


@csrf_exempt
def pagseguro_notification(request):
    notification_code = request.POST.get('notificationCode', None)
    if notification_code:
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN,
            config={'sandbox': settings.PAGSEGURO_SANDBOX}
        )
        notification_data = pg.check_notification(notification_code)
        status = notification_data.status
        reference = notification_data.reference
        try:
            order = Order.objects.get(pk=reference)
        except Order.DoesNotExist:
            pass
        else:
            order.pagseguro_update_status(status)
    return HttpResponse('OK')


class PaymentOnDeliveryView(LoginRequiredMixin, TemplateView):

    template_name = "checkout/thanks_order.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PaymentOnDeliveryView, self).get_context_data(**kwargs)
        order_pk = self.kwargs.get('pk')
        order = get_object_or_404(
            Order.objects.filter(user=self.request.user, pk=order_pk)
        )
        context['order'] = order
        return context
