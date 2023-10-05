from django.contrib import admin

from .forms import AddItemPopupForm
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_filter = ('user',)

    def get_changeform_initial_data(self, request):
        return {'user': request.user}

    def get_form(self, request, obj=None, **kwargs):
        if request.GET.get('_popup', False):
            kwargs['form'] = AddItemPopupForm

        return super().get_form(request, obj, **kwargs)
