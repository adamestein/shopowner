from django.contrib import admin

from .models import Inventory, Vendor


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_filter = ('user',)


admin.site.register(Vendor)
