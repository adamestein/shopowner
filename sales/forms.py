from django import forms

from sales.models import Sale, Tax

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ("user",)

    def __init__(self, user=None, **kwargs):
        initial = kwargs.get("initial", {})

        # Store the current tax rate (obviously, in a real application, getting
        # the tax would need to get the county and state from somwhere instead
        # of being hardcoded here
        initial["tax_rate"] = Tax.objects.get(county="Monroe", state="NY").sales_tax

        super(SalesForm, self).__init__(**kwargs)

        if user:
            self.fields["item"].queryset = self.fields["item"].queryset.filter(
                user=user
            ).exclude(
               sale__isnull = False
            )

