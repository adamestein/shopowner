from django.apps import apps
from django.contrib import admin
from django.contrib.auth.decorators import login_required


@login_required
def popup_form(request, app_label, model_name):
    # noinspection PyProtectedMember
    modeladmin = admin.site._registry[apps.get_model(app_label, model_name)]
    return modeladmin.changeform_view(request, None)
