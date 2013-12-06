from common.views.generic import AJAXView
from inventory.models import Item
from sales.utils import calculate_sale_price, round_currency

class UpdateSaleValues(AJAXView):
    def get_context_data(self, **kwargs):
        item = Item.objects.get(pk=self.request.GET["item"])

        discount = float(self.request.GET["discount"])
        item_price = float(item.price)
        tax_rate = float(self.request.GET["tax_rate"])

        percent_loc = item.commission.find("%")
        if percent_loc == -1:
            # Commission is a flat rate
            commission = float(item.commission)
        else:
            # Commission is a percentage of the item price (before sales tax)
            commission = item_price*(float(item.commission[0:percent_loc])/100.0)

        return {
            "commission": round_currency(commission),
            "price": calculate_sale_price(item_price, discount, tax_rate)
        }

