from django.conf.urls import url
from django.urls import reverse_lazy

from .forms import CreateOrderForm, UpdateOrderForm
from .models import Order
from .views import CreateOrderView, FetchInventory, ReportView, UpdateOrderListView, UpdateOrderView

app_name = 'orders'
urlpatterns = [
    url(
        r'^create/$',
        CreateOrderView.as_view(
            action='Create',
            form_class=CreateOrderForm,
            model=Order,
            success_message='Order has been created',
            success_url=reverse_lazy('orders:create'),
            template_name='orders/form.html'
        ),
        name='create'
    ),

    # url(
    #     r'^quick/$',
    #     QuickQuantityUpdateView.as_view(
    #         model=Inventory,
    #         template_name='inventory/quick_quantity_update_list.html'
    #     ),
    #     name='quick_quantity_update'
    # ),

    url(
        r'^fetch/inventory/$',
        FetchInventory.as_view(),
        name='fetch_inventory'
    ),
    url(
        r'^report/$',
        ReportView.as_view(
            model=Order,
            template_name='reports/orders.html'
        ),
        name='report'
    ),

    # url(
    #     r'^save/quantity/$',
    #     SaveQuantityValue.as_view(),
    #     name='save_quantity_values'
    # ),

    url(
        r'^update/$',
        UpdateOrderListView.as_view(
            model=Order,
            template_name='orders/update_list.html'
        ),
        name='list'
    ),

    url(
        r'^update/(?P<pk>[\d]+)$',
        UpdateOrderView.as_view(
            action='Update',
            form_class=UpdateOrderForm,
            model=Order,
            success_message='Order has been updated',
            success_url=reverse_lazy('orders:list'),
            template_name='orders/form.html'
        ),
        name='update'
    )
]
