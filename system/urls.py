from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# Admin URL patterns
urlpatterns = patterns('',
    url(r'^shopowner/admin/tools/', include('admintools.urls')),
    url(r'^shopowner/admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^shopowner/admin/', include(admin.site.urls)),
)

# Account URL patterns
urlpatterns += patterns('',
    url(r'^shopowner/accounts/login/$', 'django.contrib.auth.views.login',
        {"extra_context": {"title": "User Login"}}),
    url(r'^shopowner/accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
)

from common.views.generic import NavigationListView, NavigationTemplateView
from common.navigation import Navigation

# Top level shop owner page
urlpatterns += patterns('',
    url(r'^shopowner/$', NavigationTemplateView.as_view(
        navigation = Navigation(""),
        template_name = "home.html"
    )),
)

from common.views.generic import NavigationCreateView
from inventory.models import Seller
from inventory.navigation import Navigation as InventoryNavigation

# Inventory
urlpatterns += patterns('',
    url(r'^shopowner/inventory/$', NavigationTemplateView.as_view(
        navigation = Navigation("inventory"),
        template_name = "inventory_home.html"
    )),

    url(r'^shopowner/seller/add/$', NavigationCreateView.as_view(
        action = "Add",
        model = Seller,
        navigation = Navigation("add_seller"),
        success_url = "../updated/",
        template_name = "seller_form.html"
    )),

    url(r'^shopowner/seller/list/$', NavigationListView.as_view(
        model = Seller,
        navigation = InventoryNavigation("list_sellers"),
        template_name = "seller_list.html"
    )),

    url(r'^shopowner/seller/updated/$', NavigationTemplateView.as_view(
        navigation = InventoryNavigation(""),
        template_name = "seller_updated.html"
    ))
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^(?P<path>(css|js)/.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )

