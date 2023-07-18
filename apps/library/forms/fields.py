from django import forms
from django.core.exceptions import ValidationError

from library.forms.widgets import InlineFormset


class FormsetField(forms.Field):
    default_widget = InlineFormset
    default_error_messages = {
        'invalid': 'Enter a whole number.',
    }

    def __init__(self, **kwargs):
        self.widget = self.default_widget(kwargs.pop('formset'))
        super().__init__(**kwargs)

    def clean(self, value):
        if value is None:
            raise ValidationError(self.error_messages['invalid'], code='min_value')
        elif self.required and len(value.cleaned_data) == 0:
            raise ValidationError(self.error_messages['required'], code='required')
        return value

    def create_widget(self, formset, **kwargs):
        self.widget = self.default_widget(formset, **kwargs)
