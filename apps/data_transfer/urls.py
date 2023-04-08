from django.conf.urls import url

from .import_data import ImportView

app_name = 'data_transfer'
urlpatterns = [
    url(r'^import/$', ImportView.as_view(), name='import')
]
