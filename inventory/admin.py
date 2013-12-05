from django.contrib import admin

from forms import ItemEditForm
from models import *

class ItemAdmin(admin.ModelAdmin):
    form = ItemEditForm
    list_filter = ("user",)

class SellerAdmin(admin.ModelAdmin):
    list_filter = ("user",)

admin.site.register(Item, ItemAdmin)
admin.site.register(Seller, SellerAdmin)

