# coding=utf-8

from django.test import Client, TestCase
from django.urls import reverse
from django.conf import settings
from model_mommy import mommy
from apps.checkout.models import CartItem


class CreateCartItemTestCase(TestCase):

    def setUp(self):
        self.product = mommy.make('catalog.Product')
        self.client = Client()
        self.url = reverse(
            'checkout:create-cartitem', kwargs={'slug': self.product.slug}
        )

    def tearDown(self):
        self.product.delete
        CartItem.objects.all().delete()

    def test_add_cart_item_simple(self):
        response = self.client.get(self.url)
        redirect_url = reverse('checkout:cart-item')
        self.assertRedirects(response, redirect_url)
        self.assertEquals(CartItem.objects.count(), 1)

    def test_add_cart_item_complex(self):
        response = self.client.get(self.url)
        response = self.client.get(self.url)
        cart_item = CartItem.objects.get()
        self.assertEquals(cart_item.quantity, 2)


class CheckoutViewTesteCase(TestCase):

    def setUp(self):
        self.user = mommy.prepare(settings.AUTH_USER_MODEL)
        self.user.set_password('123')
        self.user.save()
        self.cart_item = mommy.make(CartItem)
        self.client = Client()
        self.checkout_url = reverse('checkout:checkout')

    def test_checkout_view(self):
        response = self.client.get(self.checkout_url)
        redirect_url = '{}?next={}'.format(
            reverse(settings.LOGIN_URL), self.checkout_url
        )
        self.assertRedirects(response, redirect_url)
        self.client.login(email=self.user.email, password='123')
        self.cart_item.cart_key = self.client.session.session_key
        self.cart_item.save()
        response = self.client.get(self.checkout_url)
        self.assertTemplateUsed(response, 'checkout/checkout.html')


