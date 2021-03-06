from django import forms

from common.forms.widgets import DateWidget, TextInputWithImage
from sales.models import Sale, Tax


class SalesEditForm(forms.ModelForm):
    error_css_class = "errors"

    class Meta:
        model = Sale
        exclude = ("user",)
        widgets = {
            "date": DateWidget(),
            "discount": TextInputWithImage()
        }

    # Override so we can remove the "user" value
    # noinspection PyUnusedLocal
    def __init__(self, user=None, **kwargs):
        super(SalesEditForm, self).__init__(**kwargs)

        # Only want to change the existing widgets to readonly, so it's easier
        # to do it here than figure out the widget to set it to in the Meta
        # section
        self.fields["commission"].widget.attrs["readonly"] = "readonly"
        self.fields["price"].widget.attrs["readonly"] = "readonly"


class SaleEditListForm(forms.Form):
    sales = forms.ModelChoiceField(
        queryset=Sale.objects.all(),
        empty_label="<Choose a sale>"
    )

    def __init__(self, user=None, **kwargs):
        super(SaleEditListForm, self).__init__(**kwargs)

        if user:
            self.fields["sales"].queryset = Sale.objects.filter(user=user)


class SalesForm(SalesEditForm):
    def __init__(self, user=None, **kwargs):
        initial = kwargs.get("initial", {})

        # Store the current tax rate (obviously, in a real application, getting
        # the tax would need to get the county and state from somewhere instead
        # of being hardcoded here
        try:
            initial["tax_rate"] = Tax.objects.get(county="Monroe", state="NY").sales_tax
        except Tax.DoesNotExist:
            # Can't get the tax rate automatically, so the user will have to
            # fill it in
            pass

        super(SalesForm, self).__init__(**kwargs)

        if user:
            self.fields["item"].queryset = self.fields["item"].queryset.filter(
                user=user
            ).exclude(
                sale__isnull=False
            )

    def clean_commission(self):
        data = self.cleaned_data["commission"]

        # If the commission value from the form equals "N/A" (the value put there by UpdateSaleValues() if
        # the commission on the item is not set), then make the commission in the sales object None as well
        if data is None:
            data = 0

        return data
