from common.views.generic import AJAXView
from inventory.models import Item
from sales.utils import calculate_sale_price

class SalePriceView(AJAXView):
    def get_context_data(self, **kwargs):
        discount = float(self.request.GET["discount"])
        item_price = float(Item.objects.get(pk=self.request.GET["item"]).price)
        tax_rate = float(self.request.GET["tax_rate"])

        return { "price": calculate_sale_price(item_price, discount, tax_rate) }

