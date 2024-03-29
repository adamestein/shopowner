from django.conf.urls import url
from django.urls import reverse_lazy

from .forms import AddItemForm, UpdateItemForm
from .models import Inventory
from .views import (
    AddInventoryView, QuickQuantityUpdateView, ReportView, SaveQuantityValue, UpdateInventoryListView,
    UpdateInventoryView
)

app_name = 'inventory'
urlpatterns = [
    url(
        r'^add/$',
        AddInventoryView.as_view(
            action='Add',
            form_class=AddItemForm,
            model=Inventory,
            success_message='Item "%(label)s" has been added',
            success_url=reverse_lazy('inventory:add'),
            template_name='inventory/form.html'
        ),
        name='add'
    ),

    url(
        r'^quick/$',
        QuickQuantityUpdateView.as_view(
            model=Inventory,
            template_name='inventory/quick_quantity_update_list.html'
        ),
        name='quick_quantity_update'
    ),

    url(
        r'^report/$',
        ReportView.as_view(
            model=Inventory,
            template_name='reports/inventory.html'
        ),
        name='report'
    ),

    url(
        r'^save/quantity/$',
        SaveQuantityValue.as_view(),
        name='save_quantity_values'
    ),

    url(
        r'^update/$',
        UpdateInventoryListView.as_view(
            model=Inventory,
            template_name='inventory/update_list.html'
        ),
        name='list'
    ),

    url(
        r'^update/(?P<pk>[\d]+)$',
        UpdateInventoryView.as_view(
            action='Update',
            form_class=UpdateItemForm,
            model=Inventory,
            success_message='Item "%(label)s" has been updated',
            success_url=reverse_lazy('inventory:list'),
            template_name='inventory/form.html'
        ),
        name='update'
    )
]
