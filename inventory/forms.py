from db_file_storage.form_widgets import DBClearableFileInput
from django import forms

from inventory.models import Item, Seller

class ItemEditForm(forms.ModelForm):
    # Only put active sellers in this choice
    owner = forms.ModelMultipleChoiceField(
        queryset = Seller.objects.filter(remove=False),
        help_text = "Seller(s) of this item",
    )

    class Meta:
        model = Item
        exclude = ("user",)
        widgets = {
            "picture": DBClearableFileInput
        }

class ItemAddForm(ItemEditForm):
    def __init__(self, *args, **kwargs):
        try:
            number = int(Item.objects.latest("id").number) + 1
        except ValueError:
            pass
        else:
            initial = kwargs.get("initial", {})
            initial["number"] = number
            kwargs["initial"] = initial

        super(ItemAddForm, self).__init__(*args, **kwargs)
    class Meta(ItemEditForm.Meta):
        exclude = ("user", "remove")

class ItemEditListForm(forms.Form):
    item = forms.ModelChoiceField(
        queryset = Item.objects.all(),
        empty_label = "<Choose an item>"
    )

    def __init__(self, user=None, **kwargs):
        super(ItemEditListForm, self).__init__(**kwargs)

        if user:
            self.fields["item"].queryset = Item.objects.filter(user=user)

class SellerEditListForm(forms.Form):
    seller = forms.ModelChoiceField(
        queryset = Seller.objects.all(),
        empty_label = "<Choose a seller>"
    )

    def __init__(self, user=None, **kwargs):
        super(SellerEditListForm, self).__init__(**kwargs)

        if user:
            self.fields["seller"].queryset = Seller.objects.filter(user=user)

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        exclude = ("remove", "user")   # Don't need to see on an 'Add' form

