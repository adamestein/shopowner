from django.http import HttpResponseRedirect

from .models import Order

from library.views.generic import AppCreateView, AppListView, AppTemplateView, AppUpdateView
from library.views.generic.mixins.ajax import AJAXResponseMixin


class CreateOrderView(AppCreateView):
    object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        for item in form.cleaned_data['items'].save(commit=False):
            item.order = self.object
            item.save()

        if self.success_message:
            self.success_message = self.success_message % form.cleaned_data

        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


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


class UpdateOrderListView(AppListView):
    pass


class UpdateOrderView(AppUpdateView):
    object = None

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        for item in form.cleaned_data['items'].deleted_forms:
            item.instance.delete()

        for item in form.cleaned_data['items'].save(commit=False):
            item.order = self.object
            item.save()

        if self.success_message:
            self.success_message = self.success_message % form.cleaned_data

        return HttpResponseRedirect(self.get_success_url())

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

