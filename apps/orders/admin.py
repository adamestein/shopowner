from django.contrib import admin

from .models import Order, PaymentMethod


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_filter = ('user',)


admin.site.register(PaymentMethod)
