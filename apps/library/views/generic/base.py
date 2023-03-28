from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import FormView, TemplateView


class AppFormView(LoginRequiredMixin, FormView):
    pass


class AppTemplateView(LoginRequiredMixin, TemplateView):
    pass
