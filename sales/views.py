from common.views.generic import AJAXView
from inventory.models import Item
from sales.utils import calculate_sale_price, round_currency


# noinspection PyUnresolvedReferences
class UpdateSaleValues(AJAXView):
    def get_context_data(self, **kwargs):
        item = Item.objects.get(pk=self.request.GET["item"])

        discount = float(self.request.GET["discount"])
        item_price = float(item.price)
        tax_rate = float(self.request.GET["tax_rate"])

        if "sale_price" in self.request.GET:
            # Handle the case where the item price is overriden. In this case, we're given the
            # final sale price.  In order for the rest of this function work, we need the
            # list price of the item.  To do that, we need to remove the sales tax (which gets
            # us the taxable price) and then add any discount to that to get what would have been
            # the list price.
            item_price = float(self.request.GET["sale_price"]) / (1.0 + tax_rate / 100.0)
            item_price /= 1.0 - discount / 100.0

        if item.commission:
            percent_loc = item.commission.find("%")
            if percent_loc == -1:
                # Commission is a flat rate
                commission = float(item.commission)
            else:
                # Commission is a percentage of the item price (before sales tax)
                commission = item_price * (float(item.commission[0:percent_loc]) / 100.0)

            commission = round_currency(commission)
        else:
            commission = "N/A"

        return {
            "commission": commission,
            "price": calculate_sale_price(item_price, discount, tax_rate)
        }

