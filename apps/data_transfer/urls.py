from django.conf.urls import url

from data_transfer.import_data.inventory import ImportView

app_name = 'data_transfer'
urlpatterns = [
    url(r'^import/inventory/$', ImportView.as_view(), name='import_inventory')
]
