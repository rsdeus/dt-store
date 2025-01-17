from django import forms
from django.forms import formset_factory
from django.forms.models import modelformset_factory

from apps.checkout.models import CartItem, ShippingMethods, PaymentMethods
from apps.accounts.models import UserAddress


class CartItemForm(forms.ModelForm):

    class Meta:
        model = CartItem
        fields = ['quantity']


CartItemFormSet = modelformset_factory(CartItem, form=CartItemForm, can_delete=True, extra=0)


UserShippingAddressFormSet = modelformset_factory(UserAddress, fields=['street_number',], extra=0)


ShippingMethodsFormSet = modelformset_factory(ShippingMethods, fields=['shipping_method',], extra=0)


PickupDayShippingMethodFormSet = modelformset_factory(ShippingMethods, fields=['shipping_pickup_day',], extra=0)


class DeliveryByCorreiosShippingMethodForm(forms.Form):

    postal_code = forms.CharField()
    postal_code.label = 'CEP'


DeliveryByCorreiosShippingMethodFormSet = formset_factory(form=DeliveryByCorreiosShippingMethodForm)


class PaymentMethodForm(forms.Form):

    payment_option = forms.ChoiceField(choices=PaymentMethods.PAYMENT_OPTION_CHOICES)
    payment_option.label = 'Formas de Pagamento'


PaymentMethodFormSet = formset_factory(form=PaymentMethodForm)
