from django import forms
from django.conf import settings

DEFAULT_ALT = "Add Another %(field)s"
DEFAULT_ONCLICK = "return showAddAnotherPopup(this);"
DEFAULT_URL = "/popup_add/%(field)s"

class SelectWithAdd(forms.Select):
    def __init__(self, attrs=None, choices=()):
        if attrs:
            alt = attrs.pop("alt", DEFAULT_ALT)
            onclick = attrs.pop("onclick", DEFAULT_ONCLICK)
            url = attrs.pop("url", DEFAULT_URL)
        else:
            alt = DEFAULT_ALT
            onclick = DEFAULT_ONCLICK
            url = DEFAULT_URL

        super(SelectWithAdd, self).__init__(attrs)

        self.popup_add = '<a href="' + url + '" ' + \
                         'class="add-another" ' + \
                         'id="add_id_%(field)s" ' + \
                         'onclick="' + onclick + '"> ' + \
                         '<img src="%(static_url)sadmin/img/icon_addlink.gif" ' + \
                         'width="10" height="10" alt="' + alt + '"/> </a>'

    def render(self, name, value, attrs=None, choices=()):
        html = super(SelectWithAdd, self).render(name, value, attrs, choices)

        return html+self.popup_add % {"field": name, "static_url": settings.STATIC_URL}

