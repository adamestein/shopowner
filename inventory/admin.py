from django.contrib import admin

from models import *

class ItemAdmin(admin.ModelAdmin):
    list_filter = ("user",)

admin.site.register(Item, ItemAdmin)
admin.site.register(Seller)

