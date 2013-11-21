from django.conf import settings
from django.conf.urls import patterns, include, url

from common.navigation import Navigation
from common.views.generic import *
from inventory.forms import ItemEditListForm, ItemAddForm, ItemEditForm
from inventory.forms import SellerEditForm, SellerEditListForm, SellerForm
from inventory.models import Item, Seller
from inventory.navigation import Navigation as InventoryNavigation
from sales.forms import SalesForm
from sales.navigation import Navigation as SalesNavigation
from sales.views import SalePriceView

from django.contrib import admin
admin.autodiscover()

# Use the prefix under the local Django development server
if settings.REMOTE_SERVER == False:
    prefix = "shopowner/"
else:
    prefix = ""

urlpatterns = patterns('',
    # Admin URL patterns
    url(r'^%sadmin/tools/' % prefix, include('admintools.urls')),
    url(r'^%sadmin/doc/' % prefix, include('django.contrib.admindocs.urls')),
    url(r'^%sadmin/' % prefix, include(admin.site.urls)),

    # Account URL patterns
    url(r'^%saccounts/login/$' % prefix, 'django.contrib.auth.views.login',
        {"extra_context": {"title": "User Login"}}),
    url(r'^%saccounts/logout/$' % prefix, 'django.contrib.auth.views.logout_then_login'),

    # Filesystem for images
    url(r'^%sfiles/' % prefix, include('db_file_storage.urls')),

    # Top level shop owner page
    url(r'^%s$' % prefix, NavigationTemplateView.as_view(
        navigation = Navigation(""),
        template_name = "home.html"
    )),

    # Inventory
    url(r'^%sinventory/$' % prefix, NavigationTemplateView.as_view(
        navigation = InventoryNavigation("inventory"),
        template_name = "inventory_home.html"
    )),

    url(r'^%sinventory/add/$' % prefix, NavigationCreateView.as_view(
        action = "Add",
        form_class = ItemAddForm,
        model = Item,
        navigation = InventoryNavigation("add_item"),
        success_url = "../updated/",
        template_name = "item_form.html"
    )),

    url(r'^%sinventory/edit/$' % prefix, NavigationFormView.as_view(
        form_class = ItemEditListForm,
        navigation = InventoryNavigation("edit_item"),
        template_name = "item_edit_list.html"
    )),

    url(r'^%sinventory/edit/(?P<pk>[\d]+)$' % prefix, NavigationUpdateView.as_view(
        form_class = ItemEditForm,
        model = Item,
        navigation = InventoryNavigation("edit_item"),
        success_url = "../updated/",
        template_name = "item_form.html"
    )),

    url(r'^%sinventory/list/$' % prefix, NavigationListView.as_view(
        model = Item,
        navigation = InventoryNavigation("list_items"),
        queryset = Item.objects.filter(remove=False),
        template_name = "item_list.html"
    )),

    url(r'^%sinventory/updated/$' % prefix, NavigationTemplateView.as_view(
        navigation = InventoryNavigation(""),
        template_name = "item_updated.html"
    )),

    url(r'^%sseller/add/$' % prefix, NavigationCreateView.as_view(
        action = "Add",
        form_class = SellerForm,
        navigation = InventoryNavigation("add_seller"),
        success_url = "../updated/",
        template_name = "seller_form.html"
    )),

    url(r'^%sseller/edit/$' % prefix, NavigationFormView.as_view(
        form_class = SellerEditListForm,
        navigation = InventoryNavigation("edit_seller"),
        template_name = "seller_edit_list.html"
    )),

    url(r'^%sseller/edit/(?P<pk>[\d]+)$' % prefix, NavigationUpdateView.as_view(
        form_class = SellerEditForm,
        model = Seller,
        navigation = InventoryNavigation("edit_seller"),
        success_url = "../updated/",
        template_name = "seller_form.html"
    )),

    url(r'^%sseller/list/$' % prefix, NavigationListView.as_view(
        model = Seller,
        navigation = InventoryNavigation("list_sellers"),
        queryset = Seller.objects.filter(remove=False),
        template_name = "seller_list.html"
    )),

    url(r'^%sseller/updated/$' % prefix, NavigationTemplateView.as_view(
        navigation = InventoryNavigation(""),
        template_name = "seller_updated.html"
    )),

    # Sales
    url(r'^%ssales/$' % prefix, NavigationTemplateView.as_view(
        navigation = SalesNavigation("sales"),
        template_name = "sales_home.html"
    )),

    url(r'^%ssales/price/$' % prefix, SalePriceView.as_view()),

    url(r'^%ssales/record/$' % prefix, NavigationCreateView.as_view(
        action = "Record",
        form_class = SalesForm,
        navigation = SalesNavigation("record_sale"),
        success_url = "../updated/",
        template_name = "sales_form.html"
    )),

    url(r'^%ssales/updated/$' % prefix, NavigationTemplateView.as_view(
        navigation = SalesNavigation(""),
        template_name = "sales_updated.html"
    )),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^(?P<path>(css|js)/.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )

