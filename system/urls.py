from django.conf import settings
from django.conf.urls import patterns, include, url

from common.navigation import Navigation
from common.views.generic import *
from inventory.forms import ItemEditListForm, ItemAddForm, ItemEditForm
from inventory.forms import SellerEditListForm, SellerForm
from inventory.models import Item, Seller
from inventory.navigation import Navigation as InventoryNavigation

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Admin URL patterns
    url(r'^shopowner/admin/tools/', include('admintools.urls')),
    url(r'^shopowner/admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^shopowner/admin/', include(admin.site.urls)),

    # Account URL patterns
    url(r'^shopowner/accounts/login/$', 'django.contrib.auth.views.login',
        {"extra_context": {"title": "User Login"}}),
    url(r'^shopowner/accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),

    # Filesystem for images
    url(r'^files/', include('db_file_storage.urls')),

    # Top level shop owner page
    url(r'^shopowner/$', NavigationTemplateView.as_view(
        navigation = Navigation(""),
        template_name = "home.html"
    )),

    # Inventory
    url(r'^shopowner/inventory/$', NavigationTemplateView.as_view(
        navigation = InventoryNavigation("inventory"),
        template_name = "inventory_home.html"
    )),

    url(r'^shopowner/inventory/add/$', NavigationCreateView.as_view(
        action = "Add",
        form_class = ItemAddForm,
        model = Item,
        navigation = InventoryNavigation("add_item"),
        success_url = "../updated/",
        template_name = "item_form.html"
    )),

    url(r'^shopowner/inventory/edit/$', NavigationFormView.as_view(
        form_class = ItemEditListForm,
        navigation = InventoryNavigation("edit_item"),
        template_name = "item_edit_list.html"
    )),

    url(r'^shopowner/inventory/edit/(?P<pk>[\d]+)$', NavigationUpdateView.as_view(
        form_class = ItemEditForm,
        model = Item,
        navigation = InventoryNavigation("edit_item"),
        success_url = "../updated/",
        template_name = "item_form.html"
    )),

    url(r'^shopowner/inventory/list/$', NavigationListView.as_view(
        model = Item,
        navigation = InventoryNavigation("list_items"),
        queryset = Item.objects.filter(remove=False),
        template_name = "item_list.html"
    )),

    url(r'^shopowner/inventory/updated/$', NavigationTemplateView.as_view(
        navigation = InventoryNavigation(""),
        template_name = "item_updated.html"
    )),

    url(r'^shopowner/seller/add/$', NavigationCreateView.as_view(
        action = "Add",
        form_class = SellerForm,
        navigation = InventoryNavigation("add_seller"),
        success_url = "../updated/",
        template_name = "seller_form.html"
    )),

    url(r'^shopowner/seller/edit/$', NavigationFormView.as_view(
        form_class = SellerEditListForm,
        navigation = InventoryNavigation("edit_seller"),
        template_name = "seller_edit_list.html"
    )),

    url(r'^shopowner/seller/edit/(?P<pk>[\d]+)$', NavigationUpdateView.as_view(
        model = Seller,
        navigation = InventoryNavigation("edit_seller"),
        success_url = "../updated/",
        template_name = "seller_form.html"
    )),

    url(r'^shopowner/seller/list/$', NavigationListView.as_view(
        model = Seller,
        navigation = InventoryNavigation("list_sellers"),
        queryset = Seller.objects.filter(remove=False),
        template_name = "seller_list.html"
    )),

    url(r'^shopowner/seller/updated/$', NavigationTemplateView.as_view(
        navigation = InventoryNavigation(""),
        template_name = "seller_updated.html"
    ))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^(?P<path>(css|js)/.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )

