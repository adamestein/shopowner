from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, url

from common.views.generic import *

from ..forms import SellerEditForm, SellerEditListForm, SellerForm
from ..models import Seller
from ..navigation import navigation

urlpatterns = patterns(
    'seller',

    url(
        r'^add/$',
        NavigationCreateView.as_view(
            action="Add",
            form_class=SellerForm,
            navigation=navigation("add_seller"),
            success_url=reverse_lazy("seller_add"),
            template_name="seller_form.html",
            message="<em>Sellers List</em> has been updated"
        ),
        name="seller_add"
    ),

    url(
        r'^edit/$',
        NavigationFormView.as_view(
            form_class=SellerEditListForm,
            navigation=navigation("edit_seller"),
            template_name="seller_edit_list.html"
        )
    ),

    url(
        r'^edit/(?P<pk>[\d]+)$',
        NavigationUpdateView.as_view(
            form_class=SellerEditForm,
            model=Seller,
            navigation=navigation("edit_seller"),
            success_url="../updated/",
            template_name="seller_form.html"
        ),
        name="edit_specific_seller"
    ),

    url(
        r'^list/$',
        NavigationListView.as_view(
            model=Seller,
            navigation=navigation("list_sellers"),
            queryset=Seller.objects.filter(remove=False),
            template_name="seller_list.html"
        )
    ),

    url(
        r'^updated/$',
        NavigationTemplateView.as_view(
            navigation=navigation(""),
            template_name="seller_updated.html"
        )
    ),
)
