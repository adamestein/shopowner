from django.contrib import admin

from models import *

class ConstantAdmin(admin.ModelAdmin):
    list_filter = ("user",)

admin.site.register(Constant, ConstantAdmin)

