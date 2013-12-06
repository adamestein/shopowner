from django import forms
from django.test import TestCase

from inventory.forms import ItemEditForm

class FormsTestCase(TestCase):
    def test_CleanCommission(self):
        form = ItemEditForm()

        # Commission is an integer
        form.cleaned_data = {"commission": "10"}
        self.assertEqual(form.clean_commission(), "10")

        # Commission is a floating point value
        form.cleaned_data = {"commission": "10.12"}
        self.assertEqual(form.clean_commission(), "10.12")

        # Commission is an integer percentage
        form.cleaned_data = {"commission": "10%"}
        self.assertEqual(form.clean_commission(), "10%")

        # Commission is a floating point percentage
        form.cleaned_data = {"commission": "10.12%"}
        self.assertEqual(form.clean_commission(), "10.12%")

        # Non-valid values
        form.cleaned_data = {"commission": "x10"}
        self.assertRaises(forms.ValidationError, form.clean_commission)

        # More than one decimal point
        form.cleaned_data = {"commission": "1.2.3"}
        self.assertRaises(forms.ValidationError, form.clean_commission)

        # Percent sign in wrong place
        form.cleaned_data = {"commission": "1%0"}
        self.assertRaises(forms.ValidationError, form.clean_commission)

