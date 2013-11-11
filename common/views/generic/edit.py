from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, FormView, UpdateView

class NavigationCreateView(CreateView):
    action = "Create"
    navigation = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NavigationCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NavigationCreateView, self).get_context_data(**kwargs)

        # Add action
        context["action"] = self.action

        # Add web page navigation and version info
        context["navigation"] = self.navigation

        return context

class NavigationFormView(FormView):
    navigation = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NavigationFormView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NavigationFormView, self).get_context_data(**kwargs)

        # Add web page navigation and version info
        context["navigation"] = self.navigation

        return context

class NavigationUpdateView(UpdateView):
    action = "Update"
    navigation = None

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NavigationUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NavigationUpdateView, self).get_context_data(**kwargs)

        # Add action
        context["action"] = self.action

        # Add web page navigation and version info
        context["navigation"] = self.navigation

        return context

