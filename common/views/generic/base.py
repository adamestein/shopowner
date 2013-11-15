from django.views.generic import TemplateView

from mixins import NavigationContextMixin

class NavigationTemplateView(NavigationContextMixin, TemplateView):
    pass

