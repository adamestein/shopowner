import re

from db_file_storage.form_widgets import DBClearableFileInput
from django import forms
from django.http import QueryDict

from common.forms import MultipleSelectWithAdd, TextInputWithTextSpan
from inventory.models import Category, Item, Seller

class CategoryEditForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ("user",)

    # Override so we can remove the "user" value
    def __init__(self, user=None, **kwargs):
        super(CategoryEditForm, self).__init__(**kwargs)

class CategoryEditListForm(forms.Form):
    categories = forms.ModelChoiceField(
        queryset = Category.objects.all(),
        empty_label = "<Choose a category>"
    )

    def __init__(self, user=None, **kwargs):
        super(CategoryEditListForm, self).__init__(**kwargs)

        if user:
            self.fields["categories"].queryset = Category.objects.filter(user=user)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ("remove", "user")   # Don't need to see on an 'Add' form

    # Override so we can remove the "user" value
    def __init__(self, user=None, **kwargs):
        super(CategoryForm, self).__init__(**kwargs)
        self.user = user

    def clean(self):
        # Only need to check uniqueness if we have data to check, otherwise let
        # Django do it's normal form checking thing.  We need to manually check
        # since we exclude "user" from the form and so Django can't check
        # automatically.
        if "name" in self.cleaned_data:
            name = self.cleaned_data["name"]

            if Category.objects.filter(name=name, user=self.user):
                raise forms.ValidationError("You have already added this category")

        return self.cleaned_data

class ItemEditForm(forms.ModelForm):
    # Only put active categories in this choice
    categories = forms.ModelMultipleChoiceField(
        queryset = Category.objects.filter(remove=False),
        widget = MultipleSelectWithAdd(attrs={"url": "/shopowner/category/add/"}),
        help_text = 'Categories this item is in Hold down "Control", or "Command" on a Mac, to select more than one.',
    )

    # Set up commission with a widget that includes a text span
    commission = forms.CharField(
        widget = TextInputWithTextSpan(),
        help_text = "Commission on this item (use % to indicate percentage)"
    )

    # Only put active sellers in this choice
    sellers = forms.ModelMultipleChoiceField(
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
            self.fields["sellers"].queryset = self.fields["sellers"].queryset.filter(user=user)

    def clean_commission(self):
        data = self.cleaned_data["commission"]

        # Make sure value matches a floating point value with optional ending
        # percent sign
        pattern = re.compile("^[0-9]*\.?[0-9]+%?$")
        if pattern.match(data) == None:
            raise forms.ValidationError("Commission must be a number with an optional ending percent sign")

        return data

class ItemAddForm(ItemEditForm):
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
            self.fields["sellers"].queryset = self.fields["sellers"].queryset.filter(user=user)

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
    sellers = forms.ModelChoiceField(
        queryset = Seller.objects.all(),
        empty_label = "<Choose a seller>"
    )

    def __init__(self, user=None, **kwargs):
        super(SellerEditListForm, self).__init__(**kwargs)

        if user:
            self.fields["sellers"].queryset = Seller.objects.filter(user=user)

class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        exclude = ("remove", "user")   # Don't need to see on an 'Add' form

    # Override so we can remove the "user" value
    def __init__(self, user=None, **kwargs):
        super(SellerForm, self).__init__(**kwargs)
        self.user = user

    def clean(self):
        # Only need to check uniqueness if we have data to check, otherwise let
        # Django do it's normal form checking thing.  We need to manually check
        # since we exclude "user" from the form and so Django can't check
        # automatically.
        if "first_name" in self.cleaned_data and "last_name" in self.cleaned_data:
            first_name = self.cleaned_data["first_name"]
            last_name = self.cleaned_data["last_name"]

            if Seller.objects.filter(first_name=first_name, last_name=last_name, user=self.user):
                raise forms.ValidationError("You have already added this name")

        return self.cleaned_data

