from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, include, url

from common.views.generic import *

from inventory.forms import CategoryForm, CategoryEditForm, CategoryEditListForm
from inventory.forms import ItemEditListForm, ItemAddForm, ItemEditForm
from inventory.forms import SellerEditForm, SellerEditListForm, SellerForm
from inventory.models import Category, Item, Seller
from inventory.navigation import Navigation as InventoryNavigation
from inventory.views import ItemListView, ItemView, SearchView

from sales.forms import SalesEditForm, SaleEditListForm, SalesForm
from sales.models import Sale
from sales.navigation import Navigation as SalesNavigation
from sales.views import UpdateSaleValues

from django.contrib import admin
admin.autodiscover()

# Use the prefix under the local Django development server
if not settings.REMOTE_SERVER:
    prefix = "shopowner/"
else:
    prefix = ""

urlpatterns = patterns(
    '',

    # Admin URL patterns
    url(r'^%sadmin/tools/' % prefix, include('admintools.urls')),
    url(r'^%sadmin/doc/' % prefix, include('django.contrib.admindocs.urls')),
    url(r'^%sadmin/' % prefix, include(admin.site.urls)),

    # Account URL patterns
    url(r'^%saccounts/login/$' % prefix, 'django.contrib.auth.views.login',
        {"extra_context": {"title": "User Login"}}),
    url(r'^%saccounts/logout/$' % prefix, 'django.contrib.auth.views.logout',
        {"next_page": "/shopowner/"}),

    # Filesystem for images
    url(r'^%sfiles/' % prefix, include('db_file_storage.urls')),

    # Top level shop owner page
    url(
        r'^%s$' % prefix,
        NavigationTemplateView.as_view(
            template_name="home.html"
        )
    ),

    # Inventory
    url(
        r'^%sinventory/$' % prefix,
        NavigationTemplateView.as_view(
            template_name="inventory_home.html"
        )
    ),

    url(
        r'^%sinventory/add/$' % prefix,
        NavigationCreateView.as_view(
            action="Add",
            form_class=ItemAddForm,
            model=Item,
            navigation=InventoryNavigation("add_item"),
            success_url=reverse_lazy("item_add"),
            template_name="item_form.html",
            message="<em>Inventory</em> has been updated"
        ),
        name="item_add"
    ),

    url(
        r'^%sinventory/edit/$' % prefix,
        NavigationFormView.as_view(
            form_class=ItemEditListForm,
            navigation=InventoryNavigation("edit_item"),
            template_name="item_edit_list.html"
        )
    ),

    url(
        r'^%sinventory/edit/(?P<pk>[\d]+)$' % prefix,
        NavigationUpdateView.as_view(
            form_class=ItemEditForm,
            model=Item,
            navigation=InventoryNavigation("edit_item"),
            success_url="../updated/",
            template_name="item_form.html"
        ),
        name="edit_specific_item"
    ),

    url(
        r'^%sinventory/list/$' % prefix,
        ItemListView.as_view(
            model=Item,
            navigation=InventoryNavigation("list_items"),
            queryset=Item.objects.filter(remove=False),
            template_name="item_list.html"
        )
    ),

    url(
        r'^%sinventory/list/(?P<pk>[\d]+)$' % prefix,
        ItemView.as_view(
            model=Item,
            navigation=InventoryNavigation("list_items"),
            template_name="item_list.html"
        )
    ),

    url(r'^%sinventory/search/$' % prefix, SearchView.as_view(), name="search"),

    url(
        r'^%sinventory/updated/$' % prefix,
        NavigationTemplateView.as_view(
            navigation=InventoryNavigation(""),
            template_name="item_updated.html"
        )
    ),

    url(
        r'^%scategory/add/$' % prefix,
        NavigationCreateView.as_view(
            action="Add",
            form_class=CategoryForm,
            navigation=InventoryNavigation("add_category"),
            success_url=reverse_lazy("category_add"),
            template_name="category_form.html",
            message="<em>Category List</em> has been updated"
        ),
        name="category_add"
    ),

    url(
        r'^%scategory/edit/$' % prefix,
        NavigationFormView.as_view(
            form_class=CategoryEditListForm,
            navigation=InventoryNavigation("edit_category"),
            template_name="category_edit_list.html"
        )
    ),

    url(
        r'^%scategory/edit/(?P<pk>[\d]+)$' % prefix,
        NavigationUpdateView.as_view(
            form_class=CategoryEditForm,
            model=Category,
            navigation=InventoryNavigation("edit_category"),
            success_url="../updated/",
            template_name="category_form.html"
        ),
        name="edit_specific_category"
    ),

    url(
        r'^%scategory/list/$' % prefix,
        NavigationListView.as_view(
            model=Category,
            navigation=InventoryNavigation("list_categories"),
            queryset=Category.objects.filter(remove=False),
            template_name="category_list.html"
        )
    ),

    url(
        r'^%scategory/updated/$' % prefix,
        NavigationTemplateView.as_view(
            navigation=InventoryNavigation(""),
            template_name="category_updated.html"
        )
    ),

    url(
        r'^%sseller/add/$' % prefix,
        NavigationCreateView.as_view(
            action="Add",
            form_class=SellerForm,
            navigation=InventoryNavigation("add_seller"),
            success_url=reverse_lazy("seller_add"),
            template_name="seller_form.html",
            message="<em>Sellers List</em> has been updated"
        ),
        name="seller_add"
    ),

    url(
        r'^%sseller/edit/$' % prefix,
        NavigationFormView.as_view(
            form_class=SellerEditListForm,
            navigation=InventoryNavigation("edit_seller"),
            template_name="seller_edit_list.html"
        )
    ),

    url(
        r'^%sseller/edit/(?P<pk>[\d]+)$' % prefix,
        NavigationUpdateView.as_view(
            form_class=SellerEditForm,
            model=Seller,
            navigation=InventoryNavigation("edit_seller"),
            success_url="../updated/",
            template_name="seller_form.html"
        ),
        name="edit_specific_seller"
    ),

    url(
        r'^%sseller/list/$' % prefix,
        NavigationListView.as_view(
            model=Seller,
            navigation=InventoryNavigation("list_sellers"),
            queryset=Seller.objects.filter(remove=False),
            template_name="seller_list.html"
        )
    ),

    url(
        r'^%sseller/updated/$' % prefix,
        NavigationTemplateView.as_view(
            navigation=InventoryNavigation(""),
            template_name="seller_updated.html"
        )
    ),

    # Sales
    url(
        r'^%ssales/$' % prefix,
        NavigationTemplateView.as_view(
            template_name="sales_home.html"
        )
    ),

    url(
        r'^%ssales/record/$' % prefix,
        NavigationCreateView.as_view(
            action="Record",
            form_class=SalesForm,
            navigation=SalesNavigation("record_sale"),
            success_url=reverse_lazy("record_sale"),
            template_name="sales_form.html",
            message="Sale has been recorded"
        ),
        name="record_sale"
    ),

    url(
        r'^%ssales/edit/$' % prefix,
        NavigationFormView.as_view(
            form_class=SaleEditListForm,
            navigation=SalesNavigation("edit_sale"),
            template_name="sale_edit_list.html"
        )
    ),

    url(
        r'^%ssales/edit/(?P<pk>[\d]+)$' % prefix,
        NavigationUpdateView.as_view(
            form_class=SalesEditForm,
            model=Sale,
            navigation=SalesNavigation("edit_sale"),
            success_url="../updated/",
            template_name="sales_form.html"
        )
    ),

    url(r'^%ssales/update_values/$' % prefix, UpdateSaleValues.as_view(), name="update_sale_values"),

    url(
        r'^%ssales/updated/$' % prefix,
        NavigationTemplateView.as_view(
            navigation=SalesNavigation(""),
            template_name="sales_updated.html"
        )
    ),

    url(
        r'^%ssales/view/$' % prefix,
        NavigationListView.as_view(
            model=Sale,
            navigation=SalesNavigation("view_sales"),
            template_name="sales_view.html"
        )
    ),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(
            r'^' + settings.STATIC_URL[1:] + '(?P<path>.*)$',
            'django.views.static.serve',
            {
                'document_root': 'public/static',
                'show_indexes': True
            }),
    )

