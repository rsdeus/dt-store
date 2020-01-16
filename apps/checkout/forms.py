from django import forms
from django.forms import formset_factory
from django.forms.models import modelformset_factory

from apps.checkout.models import CartItem, ShippingMethods
from apps.accounts.models import UserAddress


class CartItemForm(forms.ModelForm):

    class Meta:
        model = CartItem
        fields = ['quantity',]

CartItemFormSet = modelformset_factory(CartItem, form=CartItemForm, can_delete=True, extra=0)


class UserShippingAddressForm(forms.Form):

    class Meta:
        model = UserAddress
        fields = ['street_number',]

UserShippingAddressFormSet = modelformset_factory(UserAddress, form=UserShippingAddressForm, extra=0)


class ShippingMethodsForm(forms.Form):

    shipping_method = forms.ChoiceField(choices=ShippingMethods.SHIPPING_METHODS)
    shipping_method.label = 'Formas de Entrega'

ShippingMethodsFormSet = formset_factory(form=ShippingMethodsForm)


class PickupStoreShippingMethodForm(forms.Form):

    pickup_days = ShippingMethods.store_pickup().available_pickup_days
    pickup_day = forms.TypedChoiceField(choices=pickup_days)
    pickup_day.label = 'Dias para Retirada'

PickupStoreShippingMethodFormSet = formset_factory(form=PickupStoreShippingMethodForm)


class DeliveryByCorreiosShippingMethodForm(forms.Form):

    postal_code = forms.CharField()
    postal_code.label = 'CEP'

DeliveryByCorreiosShippingMethodFormSet = formset_factory(form=DeliveryByCorreiosShippingMethodForm)