from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy

from common.views.generic import NavigationFormView, NavigationListView, NavigationTemplateView, NavigationUpdateView

from ..forms import SalesEditForm, SaleEditListForm, SalesForm
from ..models import Sale
from ..navigation import navigation
from ..views import RecordSale, UpdateSaleValues

app_name = 'sales'
urlpatterns = [
    url(
        r'^$',
        NavigationTemplateView.as_view(
            template_name="sales_home.html"
        ),
        name='sales'
    ),

    url(
        r'^record/$',
        RecordSale.as_view(
            action="Record",
            form_class=SalesForm,
            navigation=navigation('record_sale'),
            success_url=reverse_lazy('sales:record'),
            template_name="sales_form.html",
            message="Sale has been recorded"
        ),
        name='record'
    ),

    url(
        r'^edit/$',
        NavigationFormView.as_view(
            form_class=SaleEditListForm,
            navigation=navigation("edit_sale"),
            template_name="sale_edit_list.html"
        ),
        name='edit'
    ),

    url(
        r'^edit/(?P<pk>[\d]+)$',
        NavigationUpdateView.as_view(
            form_class=SalesEditForm,
            model=Sale,
            navigation=navigation("edit_sale"),
            success_url="../updated/",
            template_name="sales_form.html"
        ),
        name='edit_specific_sale'
    ),

    url(r'^update_values/$', UpdateSaleValues.as_view(), name='update_values'),

    url(
        r'^updated/$',
        NavigationTemplateView.as_view(
            navigation=navigation(""),
            template_name="sales_updated.html"
        ),
        name='updated'
    ),

    url(
        r'^view/$',
        NavigationListView.as_view(
            model=Sale,
            navigation=navigation("view_sales"),
            template_name="sales_view.html"
        ),
        name='view'
    )
]
