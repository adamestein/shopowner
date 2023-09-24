from dashing.utils import router

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.static import serve

from dashboard.widgets import QuickSummaryWidget
from dashboard.wrapper import Wrapper

router.register(QuickSummaryWidget, 'quick_summary_widget')


urlpatterns = [
    url(r'^$', Wrapper.as_view()),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^dashboard/', include(router.urls), name='dashboard'),
    url(r'^data_transfer/', include('data_transfer.urls')),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^orders/', include('orders.urls'))
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^files(?P<path>.*)$', serve, kwargs={'document_root': settings.MEDIA_ROOT})
    ]
