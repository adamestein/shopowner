from datetime import datetime

from dashing.widgets import ListWidget

from inventory.models import Inventory

from orders.models import Order


class QuickSummaryWidget(ListWidget):
    title = 'Quick Summary'

    def get_updated_at(self):
        return f'Last updated: {datetime.now().strftime("%m/%d/%Y @ %I:%M %p")}'

    def get_data(self):
        inventory = Inventory.objects.filter(user=self.request.user)

        return [
            {
                'label': 'Number of Inventory Items',
                'value': inventory.count()
            },
            {
                'label': 'Number of Orders',
                'value': Order.objects.filter(user=self.request.user).count()
            },
            {
                'label': 'Number of Vendors',
                'value': inventory.values_list('vendor').distinct().count()
            }
        ]
