from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

DEFAULT_ALT = "Add another %(field)s"
DEFAULT_ONCLICK = "return showAddAnotherPopup(this);"
DEFAULT_URL = "/popup_add/%(field)s"


def create_popup_anchor(values):
    anchor = '<a href="' + values["url"] + '" ' + \
             'class="add-another" ' + \
             'id="add_id_%(field)s" ' + \
             'onclick="' + values["onclick"] + '"> ' + \
             '<img src="%(static_url)sadmin/img/icon_addlink.gif" ' + \
             'width="10" height="10" alt="' + values["alt"] + '"/> </a>'

    return anchor


def set_popup_defaults(attrs):
    if attrs:
        defaults = {
            "alt": attrs.pop("alt", DEFAULT_ALT),
            "onclick": attrs.pop("onclick", DEFAULT_ONCLICK),
            "url": attrs.pop("url", DEFAULT_URL)
        }
    else:
        defaults = {
            "alt": DEFAULT_ALT,
            "onclick": DEFAULT_ONCLICK,
            "url": DEFAULT_URL
        }

    return defaults

# To be used with jQuery datepicker
class DateWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        return mark_safe(super(DateWidget, self).render(name, value, attrs) + '<input type="hidden" id="datepicker" />')


class SelectWithAdd(forms.Select):
    def __init__(self, attrs=None, choices=()):
        defaults = set_popup_defaults(attrs)

        super(SelectWithAdd, self).__init__(attrs, choices)

        self.popup_add = create_popup_anchor(defaults)

    def render(self, name, value, attrs=None, choices=()):
        html = super(SelectWithAdd, self).render(name, value, attrs, choices)

        return mark_safe(html + self.popup_add % {"field": name, "static_url": settings.STATIC_URL})


class MultipleSelectWithAdd(forms.SelectMultiple):
    def __init__(self, attrs=None, choices=()):
        defaults = set_popup_defaults(attrs)

        super(MultipleSelectWithAdd, self).__init__(attrs, choices)

        self.popup_add = create_popup_anchor(defaults)

    def render(self, name, value, attrs=None, choices=()):
        html = super(MultipleSelectWithAdd, self).render(name, value, attrs, choices)

        return mark_safe(html + self.popup_add % {"field": name, "static_url": settings.STATIC_URL})


class TextInputWithTextSpan(forms.TextInput):
    def render(self, name, value, attrs=None):
        html = super(TextInputWithTextSpan, self).render(name, value, attrs)

        span = '<span id="id_text_span_' + name + '" style="margin-left: .4em;"></span>'

        return mark_safe(html + span)

