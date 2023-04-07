from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView

from .mixins.modelform import AppModelFormMixin


class AppCreateView(LoginRequiredMixin, AppModelFormMixin, CreateView):
    pass


class AppUpdateView(LoginRequiredMixin, AppModelFormMixin, UpdateView):
    pass
