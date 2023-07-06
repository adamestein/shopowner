from django.http import HttpResponse

from .models import Order

from library.views.generic import AppCreateView, AppListView, AppTemplateView, AppUpdateView
from library.views.generic.mixins.ajax import AJAXResponseMixin


# class AddInventoryView(AppCreateView):
#     pass
#
#

class FetchInventory(AJAXResponseMixin, AppTemplateView):
    def get_context_data(self, **kwargs):
        order = Order.objects.get(id=self.request.GET['order_id'])
        ret = []
        for item in order.item_set.all():
            ret.append([item.item.label, item.quantity])
        return ret

# class QuickQuantityUpdateView(AppListView):
#     pass
#
#
# class SaveQuantityValue(AJAXResponseMixin, AppTemplateView):
#     content_type = 'application/json'
#
#     def get_context_data(self, **kwargs):
#         # Don't need anything returned
#         return {}
#
#     def post(self, request, *args, **kwargs):
#         item = Inventory.objects.get(id=self.request.POST['item_id'])
#         setattr(item, self.request.POST['field'], self.request.POST['new_value'])
#         item.save()
#
#         return super().post(request, *args, **kwargs)


class ReportView(AppListView):
    pass


# class UpdateInventoryListView(AppListView):
#     pass
#
#
# class UpdateInventoryView(AppUpdateView):
#     pass
