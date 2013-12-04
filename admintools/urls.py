from django.conf.urls import patterns, url

from admintools.navigation import ATNavigation
from common.views.generic import NavigationTemplateView
from dbcopy import DBCopy

urlpatterns = patterns('admintools',
    url(r'^$', NavigationTemplateView.as_view(
        template_name="at_base.html",
    )),

    url(R'^dbcopy/$', NavigationTemplateView.as_view(
        template_name="copy_choices.html",
        navigation=ATNavigation("dbcopy")
    )),

    url(r'^dbcopy/(?P<from_db>.*)/(?P<to_db>.*)/$', DBCopy.as_view(
        template_name="dbcopy.html",
        navigation=ATNavigation("base")
    )),
)

