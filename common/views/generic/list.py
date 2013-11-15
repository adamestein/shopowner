from django.views.generic import ListView

from mixins import NavigationContextMixin

class NavigationListView(NavigationContextMixin, ListView):
    def get_queryset(self):
        queryset = super(NavigationListView, self).get_queryset()

        # Need to filter by user in addition to whatever the original queryset
        # is set to
        return queryset.filter(user=self.request.user)

