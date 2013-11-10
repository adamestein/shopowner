from django.views.generic import ListView

class NavigationListView(ListView):
    navigation = None

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NavigationListView, self).get_context_data(**kwargs)

        # Add web page navigation and version info
        context["navigation"] = self.navigation

        return context

