from django import forms

from library.forms import SelectWithAdd

from .models import Inventory


class BaseItemForm(forms.ModelForm):
    class Meta:
        fields = ['label', 'stock_number', 'vendor', 'product_number', 'wholesale_price', 'qty_bought', 'notes']
        model = Inventory
        widgets = {
            'vendor': SelectWithAdd()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['notes'].required = False
        self.fields['product_number'].required = False
        self.fields['stock_number'].required = False


class AddItemForm(BaseItemForm):
    pass


class UpdateItemForm(BaseItemForm):
    class Meta(BaseItemForm.Meta):
        fields = [
            'label', 'stock_number', 'vendor', 'product_number', 'wholesale_price', 'qty_bought', 'qty_sold', 'notes',
            'deleted'
        ]
