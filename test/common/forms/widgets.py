from django.test import TestCase

from common.forms import SelectWithAdd

class WidgetsTestCase(TestCase):
    def test_SelectWithAdd(self):
        # Default values
        widget = SelectWithAdd()

        self.assertEqual(
            widget.render("foo", None),
            u'<select name="foo">\n</select><a href="/popup_add/foo" class="add-another" id="add_id_foo" onclick="return showAddPopup(this);"> <img src="/shopowner_static/admin/img/icon_addlink.gif" width="10" height="10" alt="Add Another foo"/> </a>'
        )

        # Change alt
        widget = SelectWithAdd(attrs = {"alt": "my alt"})

        self.assertEqual(
            widget.render("foo", None),
            u'<select name="foo">\n</select><a href="/popup_add/foo" class="add-another" id="add_id_foo" onclick="return showAddPopup(this);"> <img src="/shopowner_static/admin/img/icon_addlink.gif" width="10" height="10" alt="my alt"/> </a>'
        )

        # Change onclick
        widget = SelectWithAdd(attrs = {"onclick": "my onclick"})

        self.assertEqual(
            widget.render("foo", None),
            u'<select name="foo">\n</select><a href="/popup_add/foo" class="add-another" id="add_id_foo" onclick="my onclick"> <img src="/shopowner_static/admin/img/icon_addlink.gif" width="10" height="10" alt="Add Another foo"/> </a>'
        )

        # Change URL
        widget = SelectWithAdd(attrs = {"url": "my url"})

        self.assertEqual(
            widget.render("foo", None),
            u'<select name="foo">\n</select><a href="my url" class="add-another" id="add_id_foo" onclick="return showAddPopup(this);"> <img src="/shopowner_static/admin/img/icon_addlink.gif" width="10" height="10" alt="Add Another foo"/> </a>'
        )
