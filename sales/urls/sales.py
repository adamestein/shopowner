from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy

from common.views.generic import *

from ..forms import SalesEditForm, SaleEditListForm, SalesForm
from ..models import Sale
from ..navigation import Navigation as SalesNavigation
from ..views import UpdateSaleValues

app_name = 'sales'
urlpatterns = [
    url(
        r'^$',
        NavigationTemplateView.as_view(
            template_name="sales_home.html"
        )
    ),

    url(
        r'^record/$',
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
        r'^edit/$',
        NavigationFormView.as_view(
            form_class=SaleEditListForm,
            navigation=SalesNavigation("edit_sale"),
            template_name="sale_edit_list.html"
        )
    ),

    url(
        r'^edit/(?P<pk>[\d]+)$',
        NavigationUpdateView.as_view(
            form_class=SalesEditForm,
            model=Sale,
            navigation=SalesNavigation("edit_sale"),
            success_url="../updated/",
            template_name="sales_form.html"
        )
    ),

    url(r'^update_values/$', UpdateSaleValues.as_view(), name="update_sale_values"),

    url(
        r'^updated/$',
        NavigationTemplateView.as_view(
            navigation=SalesNavigation(""),
            template_name="sales_updated.html"
        )
    ),

    url(
        r'^view/$',
        NavigationListView.as_view(
            model=Sale,
            navigation=SalesNavigation("view_sales"),
            template_name="sales_view.html"
        )
    )
]