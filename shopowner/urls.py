from django.conf.urls import include, url

from common.views.generic import NavigationTemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', NavigationTemplateView.as_view(template_name="home.html"), name='home'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^files/', include('db_file_storage.urls')),
    url(r'^inventory/item/', include('inventory.urls.item')),
    url(r'^inventory/category/', include('inventory.urls.category')),
    url(r'^inventory/seller/', include('inventory.urls.seller')),
    url(r'^sales/', include('sales.urls.sales'))
]
