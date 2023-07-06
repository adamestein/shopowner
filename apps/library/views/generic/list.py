from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView


class AppListView(LoginRequiredMixin, ListView):
    def get_queryset(self):
        queryset = super().get_queryset()

        # Need to filter by user and deleted in addition to whatever the original queryset is set to
        return queryset.filter(deleted=False, user=self.request.user)
