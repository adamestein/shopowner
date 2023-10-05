from django import forms
from django.core.exceptions import ValidationError

from library.forms import FormsetField, HTML5DateInput, SelectWithAdd, SelectMultipleWithAdd

from .models import Item, Order

from inventory.models import Inventory


class ItemForm(forms.ModelForm):
    class Meta:
        exclude = ()
        model = Item
        widgets = {
            'item': SelectWithAdd(Item.item)
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['item'].queryset = Inventory.objects.filter(user=user)


ItemFormSet = forms.inlineformset_factory(Order, Item, exclude=['order'], extra=0, form=ItemForm)


class BaseOrderForm(forms.ModelForm):
    items = FormsetField(
        error_messages={
            'invalid': 'Quantity must be greater than 0',
            'required': 'Items bought in this order must be listed'
        },
        formset=ItemFormSet,
        help_text='Items bought in this order'
    )

    class Meta:
        fields = [
            'date_ordered', 'date_received', 'vendor', 'reference_number', 'items', 'net_cost', 'shipping_cost', 'tax',
            'payment_method', 'receipts', 'notes'
        ]
        model = Order
        widgets = {
            'date_ordered': HTML5DateInput(),
            'date_received': HTML5DateInput(),
            'payment_method': SelectWithAdd(Order.payment_method),
            'receipts': SelectMultipleWithAdd(
                Order.receipts, parameters={'category': 'receipt', 'directory': 'receipts'}
            ),
            'vendor': SelectWithAdd(Order.vendor)
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['items'].create_widget(ItemFormSet, form_kwargs={'instance': kwargs['instance'], 'user': user})


class CreateOrderForm(BaseOrderForm):
    update_quantity = forms.BooleanField(widget=forms.HiddenInput(), required=False)


class UpdateOrderForm(BaseOrderForm):
    class Meta(BaseOrderForm.Meta):
        fields = [
            'date_ordered', 'date_received', 'reference_number', 'vendor', 'items', 'net_cost', 'shipping_cost',
            'tax', 'payment_method', 'receipts', 'notes', 'deleted'
        ]

    def clean(self):
        cleaned_data = super().clean()

        if len(cleaned_data['items'].deleted_forms) == len(cleaned_data['items']):
            raise ValidationError('Items bought in this order must be listed', code='required')

        return cleaned_data
