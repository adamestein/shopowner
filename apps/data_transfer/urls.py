from django.conf.urls import url

from data_transfer.import_data.inventory import ImportView as ImportInventoryView
from data_transfer.import_data.orders import ImportView as ImportOrderView

app_name = 'data_transfer'
urlpatterns = [
    url(r'^import/inventory/$', ImportInventoryView.as_view(), name='import_inventory'),
    url(r'^import/orders/$', ImportOrderView.as_view(), name='import_orders')
]
