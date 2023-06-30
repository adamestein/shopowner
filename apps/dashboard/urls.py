from django.conf.urls import url

from library.views.generic import AppTemplateView

app_name = 'dashboard'
urlpatterns = [
    url(r'$', AppTemplateView.as_view(template_name='dashboard/dashboard.html'), name='home')
]
