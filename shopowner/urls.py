from django.conf.urls import include, url
from django.contrib import admin

from library.views.generic import AppTemplateView

urlpatterns = [
    url(r'^$', AppTemplateView.as_view(template_name='dashboard.html'), name='home'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^data_transfer/', include('data_transfer.urls')),
    url(r'^inventory/', include('inventory.urls'))
]
