from django import forms

from inventory.models import Item, Seller

class ItemEditListForm(forms.Form):
    item = forms.ModelChoiceField(
        queryset = Item.objects.all(),
        empty_label = "<Choose an item>"
    )

class ItemEditForm(forms.ModelForm):
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
        exclude = ("user",)

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

class SellerEditListForm(forms.Form):
    seller = forms.ModelChoiceField(
        queryset = Seller.objects.all(),
        empty_label = "<Choose a seller>"
    )

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        exclude = ("remove",)   # Don't need to see on an 'Add' form

