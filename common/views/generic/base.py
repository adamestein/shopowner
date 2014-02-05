import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.generic import TemplateView

from mixins import NavigationContextMixin


class AJAXView(TemplateView):
    def get_context_data(self, **kwargs):
        # Return what was sent in
        return kwargs

    def render_to_response(self, context, **kwargs):
        data = json.dumps(context, cls=DjangoJSONEncoder)
        kwargs["content_type"] = "application/json"

        return HttpResponse(data, kwargs)

class NavigationTemplateView(NavigationContextMixin, TemplateView):
    pass

