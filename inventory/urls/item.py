from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, url

from common.views.generic import *

from ..forms import ItemEditListForm, ItemAddForm, ItemEditForm
from ..models import Item
from ..navigation import navigation
from ..views import ItemListView, ItemView, SearchView

urlpatterns = patterns(
    'inventory',
    
    url(
        r'^$',
        NavigationTemplateView.as_view(
            template_name="inventory_home.html"
        )
    ),

    url(
        r'^add/$',
        NavigationCreateView.as_view(
            action="Add",
            form_class=ItemAddForm,
            model=Item,
            navigation=navigation("add_item"),
            success_url=reverse_lazy("item_add"),
            template_name="item_form.html",
            message="<em>Inventory</em> has been updated"
        ),
        name="item_add"
    ),

    url(
        r'^edit/$',
        NavigationFormView.as_view(
            form_class=ItemEditListForm,
            navigation=navigation("edit_item"),
            template_name="item_edit_list.html"
        )
    ),

    url(
        r'^edit/(?P<pk>[\d]+)$',
        NavigationUpdateView.as_view(
            form_class=ItemEditForm,
            model=Item,
            navigation=navigation("edit_item"),
            success_url="../updated/",
            template_name="item_form.html"
        ),
        name="edit_specific_item"
    ),

    url(
        r'^list/$',
        ItemListView.as_view(
            model=Item,
            navigation=navigation("list_items"),
            queryset=Item.objects.filter(remove=False),
            template_name="item_list.html"
        )
    ),

    url(
        r'^list/(?P<pk>[\d]+)$',
        ItemView.as_view(
            model=Item,
            navigation=navigation("list_items"),
            template_name="item_list.html"
        )
    ),

    url(
        r'^image_sheet',
        ItemListView.as_view(
            model=Item,
            navigation=navigation("image_sheet"),
            queryset=Item.objects.filter(remove=False).exclude(picture=""),
            template_name="image_sheet.html"
        )
    ),

    url(r'^search/$', SearchView.as_view(), name="search"),

    url(
        r'^updated/$',
        NavigationTemplateView.as_view(
            navigation=navigation(""),
            template_name="item_updated.html"
        )
    ),
)
