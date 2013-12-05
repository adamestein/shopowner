from db_file_storage.form_widgets import DBClearableFileInput
from django import forms

from common.forms import MultipleSelectWithAdd
from inventory.models import Item, Seller

class ItemEditForm(forms.ModelForm):
    # Only put active sellers in this choice
    seller = forms.ModelMultipleChoiceField(
        queryset = Seller.objects.filter(remove=False),
        widget = MultipleSelectWithAdd(attrs={"url": "/shopowner/seller/add/"}),
        help_text = 'Seller(s) of this item Hold down "Control", or "Command" on a Mac, to select more than one.',
    )

    class Meta:
        model = Item
        exclude = ("user",)
        widgets = {
            "picture": DBClearableFileInput
        }

    def __init__(self, user=None, *args, **kwargs):
        super(ItemEditForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["seller"].queryset = self.fields["seller"].queryset.filter(user=user)

class ItemAddForm(ItemEditForm):
    seller = forms.ModelChoiceField(
        queryset = Seller.objects.filter(remove=False),
        empty_label = None,
        widget = MultipleSelectWithAdd(attrs={"url": "/shopowner/seller/add/"}),
        help_text = 'Seller(s) of this item Hold down "Control", or "Command" on a Mac, to select more than one.',
    )

    class Meta(ItemEditForm.Meta):
        exclude = ("user", "remove")

    def __init__(self, user=None, *args, **kwargs):
        try:
            number = int(Item.objects.filter(user=user).latest("id").number) + 1
        except Item.DoesNotExist:
            # No items in database, so no latest item to get number from, so start with 1
            number = 1
        except ValueError:
            number = None # Item number isn't an integer, so we can't increment value

        if number != None:
            initial = kwargs.get("initial", {})
            initial["number"] = number
            kwargs["initial"] = initial

        super(ItemAddForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["seller"].queryset = self.fields["seller"].queryset.filter(user=user)

class ItemEditListForm(forms.Form):
    item = forms.ModelChoiceField(
        queryset = Item.objects.all(),
        empty_label = "<Choose an item>"
    )

    def __init__(self, user=None, **kwargs):
        super(ItemEditListForm, self).__init__(**kwargs)

        if user:
            self.fields["item"].queryset = Item.objects.filter(user=user)

class SellerEditForm(forms.ModelForm):
    class Meta:
        model = Seller
        exclude = ("user",)

    # Override so we can remove the "user" value
    def __init__(self, user=None, **kwargs):
        super(SellerEditForm, self).__init__(**kwargs)


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

    # Override so we can remove the "user" value
    def __init__(self, user=None, **kwargs):
        super(SellerForm, self).__init__(**kwargs)

