from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import ContextMixin
from django.views.generic.edit import ModelFormMixin

class NavigationContextMixin(ContextMixin):
    navigation = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NavigationContextMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NavigationContextMixin, self).get_context_data(**kwargs)

        # Add web page navigation and version info
        context["navigation"] = self.navigation

        return context

class NavigationEditMixin(NavigationContextMixin, ModelFormMixin):
    action = None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NavigationEditMixin, self).get_context_data(**kwargs)

        # Add action
        context["action"] = self.action

        return context

    def get_form_kwargs(self):
        kwargs = super(NavigationEditMixin, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})  # Add user so form can use value to filter

        return kwargs

