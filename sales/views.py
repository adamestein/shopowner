from common.views.generic import AJAXView
from inventory.models import Item
from sales.utils import calculate_sale_price, round_currency

class UpdateSaleValues(AJAXView):
    def get_context_data(self, **kwargs):
        item = Item.objects.get(pk=self.request.GET["item"])

        discount = float(self.request.GET["discount"])
        item_price = float(item.price)
        tax_rate = float(self.request.GET["tax_rate"])

        return {
            "commission": round_currency(item_price*(item.commission/100.0)),
            "price": calculate_sale_price(item_price, discount, tax_rate)
        }

