from django import forms

from inventory.models import Item, Seller

class ItemForm(forms.ModelForm):
    # Only put active sellers in this choice
    owner = forms.ModelMultipleChoiceField(
        queryset = Seller.objects.filter(remove=False),
        help_text = "Seller(s) of this item",
    )

    # Only as the user for the filename.  Behind the scenes, we'll upload and
    # fill in the URLField field.
    picture = forms.ImageField(
        required = False,
        help_text = "File containing this item's image"
    )

    class Meta:
        model = Item
        exclude = ("user", "remove")

class SellerEditListForm(forms.Form):
    seller = forms.ModelChoiceField(
        queryset = Seller.objects.all(),
        empty_label = "<Choose a seller>"
    )

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        exclude = ("remove",)   # Don't need to see on an 'Add' form

