from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

# Admin URL patterns
urlpatterns = patterns('',
    url(r'^booth/admin/tools/', include('admintools.urls')),
    url(r'^booth/admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^booth/admin/', include(admin.site.urls)),
)

# Account URL patterns
urlpatterns += patterns('',
    url(r'^booth/accounts/login/$', 'django.contrib.auth.views.login',
        {"extra_context": {"title": "User Login"}}),
    url(r'^booth/accounts/logout/$', 'django.contrib.auth.views.logout_then_login'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^(?P<path>(css|js)/.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )

