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

from common.views.generic import NavigationTemplateView
from common.navigation import Navigation

# Top level shop owner page
urlpatterns += patterns('',
    url(r'^shopowner/$', NavigationTemplateView.as_view(
        template_name = "home.html",
        navigation = Navigation("")
    )),
)

# Inventory
urlpatterns += patterns('',
    url(r'^shopowner/inventory/$', NavigationTemplateView.as_view(
        template_name = "inventory_home.html",
        navigation = Navigation("inventory")
    )),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^(?P<path>(css|js)/.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )

