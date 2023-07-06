from django.contrib import admin

from .models import Item, Order, PaymentMethod


class ItemInline(admin.TabularInline):
    extra = 0
    model = Item


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (ItemInline, )
    list_filter = ('user',)


admin.site.register(Item)
admin.site.register(PaymentMethod)
