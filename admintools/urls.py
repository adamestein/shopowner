from django.conf.urls import url


from .navigation import ATNavigation
from .dbcopy import DBCopy

from common.views.generic import NavigationTemplateView

app_name = 'admintools'
urlpatterns = [
    url(
        r'^$',
        NavigationTemplateView.as_view(
            template_name="at_base.html",
        )
    ),

    url(
        r'^dbcopy/$',
        NavigationTemplateView.as_view(
            template_name="copy_choices.html",
            navigation=ATNavigation("dbcopy")
        )
    ),

    url(
        r'^dbcopy/(?P<from_db>.*)/(?P<to_db>.*)/$',
        DBCopy.as_view(
            template_name="dbcopy.html",
            navigation=ATNavigation("base")
        )
    ),
]

