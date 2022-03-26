from django.conf import settings
from django.conf.urls import include, url

from common.views.generic import *

from django.contrib import admin
admin.autodiscover()

# Use the prefix under the local Django development server
if not settings.REMOTE_SERVER:
    prefix = "shopowner/"
else:
    prefix = ""

urlpatterns = [
    # Admin URL patterns
    url(r'^%sadmin/tools/' % prefix, include('admintools.urls')),
    url(r'^%sadmin/doc/' % prefix, include('django.contrib.admindocs.urls')),
    url(r'^%sadmin/' % prefix, include(admin.site.urls)),

    # Account URL patterns
    url('accounts/', include('django.contrib.auth.urls')),
    # url(r'^%saccounts/login/$' % prefix, 'django.contrib.auth.views.login',
    #     {"extra_context": {"title": "User Login"}}),
    # url(r'^%saccounts/logout/$' % prefix, 'django.contrib.auth.views.logout',
    #     {"next_page": "/shopowner/"}),

    # Filesystem for images
    url(r'^%sfiles/' % prefix, include('db_file_storage.urls')),

    # Top level shop owner page
    url(
        r'^%s$' % prefix,
        NavigationTemplateView.as_view(
            template_name="home.html"
        )
    ),

    # Inventory
    url(r'^%sinventory/' % prefix, include('inventory.urls.item')),
    url(r'^%scategory/' % prefix, include('inventory.urls.category')),
    url(r'^%sseller/' % prefix, include('inventory.urls.seller')),

    # Sales
    url(r'^%ssales/' % prefix, include('sales.urls.sales')),
]

# if settings.DEBUG:
#     urlpatterns += [
#         '',
#         url(
#             r'^' + settings.STATIC_URL[1:] + '(?P<path>.*)$',
#             'django.views.static.serve',
#             {
#                 'document_root': 'public/static',
#                 'show_indexes': True
#             }),
#     ]

