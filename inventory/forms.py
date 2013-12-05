from db_file_storage.form_widgets import DBClearableFileInput
from django import forms
from django.http import QueryDict

from common.forms import MultipleSelectWithAdd, TextInputWithTextSpan
from inventory.models import Item, Seller

class ItemEditForm(forms.ModelForm):
    # Set up commission with a widget that includes a text span
    commission = forms.FloatField(
        widget = TextInputWithTextSpan(),
        help_text = "Commission on this item (in percentage)"
    )

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
        # We set up the admin to use this form.  As a result, it doesn't send
        # the user like our own views do.  In this case, user contains the form
        # values instead of args.  If user has the form values, just move them
        # into args and set user to None so that everything down the line works
        # normally.
        if (isinstance(user, QueryDict)):
            args = (user,) + args
            user = None

        super(ItemEditForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["seller"].queryset = self.fields["seller"].queryset.filter(user=user)

class ItemAddForm(ItemEditForm):
    #seller = forms.ModelMultipleChoiceField(
    #    queryset = Seller.objects.filter(remove=False),
    #    widget = MultipleSelectWithAdd(attrs={"url": "/shopowner/seller/add/"}),
    #    help_text = 'Seller(s) of this item Hold down "Control", or "Command" on a Mac, to select more than one.',
    #)

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
        self.user = user

        if user:
            self.fields["seller"].queryset = self.fields["seller"].queryset.filter(user=user)

    def clean(self):
        number = self.cleaned_data["number"]

        if Item.objects.filter(number=number, user=self.user):
            raise forms.ValidationError("You have already added an item with this number")
        else:
            return self.cleaned_data

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
        self.user = user

    def clean(self):
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]

        if Seller.objects.filter(first_name=first_name, last_name=last_name, user=self.user):
            raise forms.ValidationError("You have already added this name")
        else:
            return self.cleaned_data

