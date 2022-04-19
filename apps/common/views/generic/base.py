import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.generic import TemplateView

from .mixins import NavigationContextMixin


class AJAXView(TemplateView):
    def render_to_response(self, context, **kwargs):
        kwargs.setdefault('content_type', self.content_type)
        return HttpResponse(json.dumps(context))


class NavigationTemplateView(NavigationContextMixin, TemplateView):
    pass

