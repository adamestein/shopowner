from django.conf.urls import url

from .models import Inventory
from .report import ReportView

app_name = 'inventory'
urlpatterns = [
    url(
        r'^report/$',
        ReportView.as_view(
            queryset=Inventory.objects.all(),
            template_name='reports/inventory.html'
        ),
        name='report'
    )
]
