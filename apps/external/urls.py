from django.conf.urls import url

from .import_data import ImportDataView

app_name = 'external'
urlpatterns = [
    url(r'^import/$', ImportDataView.as_view(), name='import_data')
]
