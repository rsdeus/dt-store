# coding=utf-8

from model_mommy.mommy import get_model
from pagseguro import PagSeguro

from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from apps.catalog.models import Product
from django.contrib.sessions.models import Session
from importlib import import_module

import requests
from bs4 import BeautifulSoup as bs
import pycep_correios

import datetime
import time
import logging

logger = logging.getLogger(__name__)


class CartItemManager(models.Manager):

    def add_item(self, cart_key, product):
        if self.filter(cart_key=cart_key, product=product).exists():
            created = False
            cart_item = self.get(cart_key=cart_key, product=product)
            cart_item.quantity = cart_item.quantity + 1
        else:
            created = True
            cart_item = CartItem(cart_key=cart_key, product=product, price=product.price, weight=product.weight)

        try:
            cart_item.save()
        except ValidationError as e:
            raise ValidationError(e.message)
        else:
            return cart_item, created

    def total(self, cart_key):
        aggregate_queryset = CartItem.objects.filter(cart_key=cart_key).aggregate(
            total=models.Sum(
                models.F('price') * models.F('quantity'),
                output_field=models.DecimalField()
            )
        )
        return float(aggregate_queryset['total'] or 0)


class CartItem(models.Model):
    
    cart_key = models.CharField('Chave do Carrinho', max_length=40, db_index=True)
    product = models.ForeignKey('catalog.Product', verbose_name='Produto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    weight = models.DecimalField('Peso', decimal_places=2, max_digits=8, default=0)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    objects = CartItemManager()
    
    class Meta:
        verbose_name = 'Item do Carrinho'
        verbose_name_plural = 'Itens dos Carrinhos'
        unique_together = (('cart_key', 'product'),)
        
    def __str__(self):
        return '{} [{}]'.format(self.product, self.quantity, self.weight)

    def save(self, *args, **kwargs):
        if self.stock_manager(self):
            return super().save(*args, **kwargs)
        else:
            return None

    def stock_manager(self, *args, **kwargs):
        if kwargs:
            if kwargs['delete']:
                cart_item = kwargs['id']
                cart_item.product.stock = cart_item.product.stock + cart_item.quantity
                cart_item.product.save()
        else:
            if CartItem.objects.filter(cart_key=self.cart_key, product=self.product).exists():
                cart_item = CartItem.objects.get(cart_key=self.cart_key, product=self.product)
                if cart_item:
                    qtd = self.quantity - cart_item.quantity
                    if qtd > 0:
                        if self.product.stock < qtd:
                            raise ValidationError("Produto com quantidade em estoque menor que a solicitada")
                        else:
                            self.product.stock = self.product.stock - qtd
                    elif qtd < 0:
                        self.product.stock = self.product.stock + abs(qtd)

                    self.product.save()
            else:
                self.product.stock = self.product.stock - self.quantity
                self.product.save()

        return True

    @staticmethod
    def return_stock_from_cart_item():
        logger.info("iniciando return_stock_cart_item")
        return_stock_items = []
        for cart_item in CartItem.objects.all():
            if not Session.objects.filter(pk=cart_item.cart_key).exists():
                return_stock_items = {'session_key': cart_item.cart_key}
                return_stock_items.update({'item.product.stock': cart_item.product.stock})
                return_stock_items.update({'item.quantity': cart_item.quantity})
                cart_item.product.stock += cart_item.quantity
                cart_item.product.save()
                cart_item.delete()
        return return_stock_items


def post_save_cart_item(instance, **kwargs):
    if instance.quantity < 1:
        instance.delete()


models.signals.post_save.connect(
    post_save_cart_item, sender=CartItem, dispatch_uid='post_save_cart_item'
)


class ShippingMethods():  # TODO: Implementar de outra forma, talvez criar o próprio app

    SHIPPING_METHODS = (
        ('none', 'Escolha a Forma de Entrega'),
        ('delivery_by_correios_sedex', 'Entrega via Correios SEDEX'),
        ('delivery_by_correios_pac', 'Entrega via Correios PAC'),
        ('store_pickup', 'Retirada na Loja'),
    )

    class store_pickup():

        shipping_cost = float(0.00)
        available_pickup_days = settings.AVAILABLE_PICKUP_DAYS
        pickup_address = settings.PICKUP_ADDRESS

        def get_shipping_cost(self):
            return self.shipping_cost

        def get_available_pickup_days(self):
            return self.available_pickup_days

        def get_pickup_address(self):
            return self.pickup_address


    class delivery_by_correios():

        endpoint_url = 'http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx/CalcPrecoPrazo?'

        def get_address_by_postal_code(self, postal_code_to):

            address = pycep_correios.consultar_cep(postal_code_to)

            return address


        def get_calculate_shipping(self, session_key, service, postal_code_from, postal_code_to):

            cart_item = CartItem.objects.filter(cart_key=session_key)

            total_weight = 0

            for product in cart_item:
                total_weight += float(product.weight * product.quantity)

            service_code = ''
            if service == 'delivery_by_correios_sedex':
                service_code = 40010
            elif service == 'delivery_by_correios_pac':
                service_code = 41106

            params = {
                'nCdEmpresa': '',
                'sDsSenha': '',
                'nCdServico': service_code,
                'sCepOrigem': postal_code_from,
                'sCepDestino': postal_code_to,
                'nVlPeso': total_weight,
                'nCdFormato': 1,
                'nVlComprimento': 15,
                'nVlLargura': 20,
                'nVlAltura': 5,
                'nVlDiametro': 0,
                'sCdMaoPropria': 'N',
                'nVlValorDeclarado': 0,
                'sCdAvisoRecebimento': 'N',
                'StrRetorno': 'XML'
            }

            response = requests.get(self.endpoint_url, params)

            if response.status_code == 200:
                xml_content = bs(response.content, "xml")

                if xml_content.MsgErro.string is None:
                    if xml_content.Valor.string is None:
                        shipping_cost = float(0.00)
                    else:
                        shipping_cost = float(str(xml_content.Valor.string.replace(",", ".")) or 0)

                    if xml_content.PrazoEntrega.string is None:
                        shipping_time = int(0)
                    else:
                        shipping_time = int(str(xml_content.PrazoEntrega.string.replace(",", ".")) or 0)

                    return shipping_cost, shipping_time
                else:
                    shipping_msg_error = xml_content.MsgErro.string

                return shipping_msg_error
            else:
                return response.status_code


    def fixed_price(self):

        shipping_cost = settings.FIXED_PRICE

        return shipping_cost


class OrderManager(models.Manager):

    def create_order(self, user, cart_items, session_key):
        SessionStore = import_module(settings.SESSION_ENGINE).SessionStore
        session = SessionStore(session_key=session_key)
        order = self.create(
            user=user,
            shipping_method=session['shipping_method'],
            shipping_pickup_day=session['pickup_day'],
            shipping_cost=session['shipping_cost'],
            shipping_time=session['shipping_time']
        )
        for cart_item in cart_items:
            order_item = OrderItem.objects.create(
                order=order,
                quantity=cart_item.quantity,
                product=cart_item.product,
                price=cart_item.price,
            )

        return order


class Order(models.Model):
    
    PAYMENT_STATUS_CHOICES = (
        (0, 'Aguardando Pagamento'),
        (1, 'Concluída'),
        (2, 'Cancelada'),
    )

    SHIPPING_STATUS_CHOICES = (
        (0, 'Aguardando Entrega'),
        (2, 'Concluída'),
    )

    SHIPPING_METHODS = ShippingMethods.SHIPPING_METHODS
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário', on_delete='CASCADE')
    payment_status = models.IntegerField(
        'Situação do Pagamento', choices=PAYMENT_STATUS_CHOICES, default=0, blank=True
    )
    shipping_status = models.IntegerField(
        'Situação da Entrega', choices=SHIPPING_STATUS_CHOICES, default=0, blank=True
    )
    shipping_method = models.CharField(
        'Forma de Entrega', max_length=30, choices=SHIPPING_METHODS
    )
    shipping_pickup_day = models.CharField(
        'Dia de Retirada', max_length=30, blank=True
    )
    shipping_cost = models.DecimalField(
        'Frete', decimal_places=2, max_digits=8, default=0
    )
    shipping_time = models.IntegerField(
        'Tempo de Entrega', default=0
    )
    shipping_tracking_code = models.CharField(
        'Código de Rastreamento', max_length=30, blank=True
    )
    order_details = models.TextField(
        'Detalhes do Pedido', max_length=255, blank=True
    )

    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    objects = OrderManager()
    
    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        
    def __str__(self):
        return 'Pedido #{}'.format(self.pk)

    def products(self):
        products_ids = self.items.values_list('product')
        return Product.objects.filter(pk__in=products_ids)

    def total(self):
        aggregate_queryset = self.items.aggregate(
            total=models.Sum(
                models.F('price') * models.F('quantity'),
                output_field=models.DecimalField()
            )
        )
        return aggregate_queryset['total']

    def total_order(self):
        total = float(self.total()) + float(self.shipping_cost)
        return total

    def pagseguro_update_status(self, status):
        if status == '3':
            self.status = 1
        elif status == '7':
            self.status = 2
        self.save()

    def complete(self):
        self.status = 1
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='Pedido', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('catalog.Product', verbose_name='Produto', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('Quantidade', default=1)
    weight = models.DecimalField('Peso', decimal_places=2, max_digits=8, default=0)
    price = models.DecimalField('Preço', decimal_places=2, max_digits=8)

    class Meta:
        verbose_name = 'Item do pedido'
        verbose_name_plural = 'Itens dos pedidos'

    def __str__(self):
        return '[{}] {}'.format(self.order, self.product)

    @staticmethod
    def return_stock_from_order():
        logger.info("Iniciando return_stock_from_order")
        delta = datetime.datetime.now() - datetime.timedelta(minutes=settings.EXPIRE_TIME)
        orders = Order.objects.filter(modified__date__lt=delta, payment_status=0)
        for order in orders:
            logger.info(order)
            for order_item in order.items.all():
                logger.info(order_item)
                if Product.objects.filter(id=order_item.product.id).exists():
                    product = Product.objects.get(id=order_item.product.id)
                    product.stock += order_item.quantity
                    logger.info('%s: %s', product, product.stock)
                    logger.info('Deleting order item %s: ', order_item)
                    order_item.delete()
                    product.save()
                else:
                    raise ValueError('Produto %s não existe mais no catálogo', order_item.product)
            order.delete()


class PaymentMethods(models.Model):
    
    class Meta:
        verbose_name = 'Método de Pagamento'
        verbose_name_plural = 'Métodos de Pagamento'
        
    PAYMENT_OPTION_CHOICES = (
        ('deposit', 'Depósito'),
        ('pagseguro', 'PagSeguro'),
        ('paypal', 'Paypal'),
        ('pagamento_entrega', 'Pagamento na Entrega'),
    )

    order = models.OneToOneField(
        Order, verbose_name='Pedido', related_name='payment_method', default=107, on_delete=models.CASCADE
    )
    payment_option = models.CharField(
        'Opção de Pagamento', choices=PAYMENT_OPTION_CHOICES, default='deposit', max_length=20
    )

    def __str__(self):
        return self.payment_option

    def pagseguro(self):
        self.payment_option = 'pagseguro'
        self.save()
        pg = PagSeguro(
            email=settings.PAGSEGURO_EMAIL, token=settings.PAGSEGURO_TOKEN,
            config={'sandbox': settings.PAGSEGURO_SANDBOX}
        )
        pg.sender = {
            'email': self.order.user.email
        }
        pg.reference_prefix = ''
        pg.shipping = {
            "type": 1,
            "street": "Av Brig Faria Lima",
            "number": 1234,
            "complement": "5 andar",
            "district": "Jardim Paulistano",
            "postal_code": "06650030",
            "city": "Sao Paulo",
            "state": "SP",
            "country": "BRA",

        }
        pg.reference = self.order.pk
        for item in self.order.items.all():
            pg.items.append(
                {
                    'id': item.product.pk,
                    'description': item.product.name,
                    'quantity': item.quantity,
                    'amount': '%.2f' % item.price,
                    'weight': '1000'
                }
            )
        return pg
