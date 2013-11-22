from common.views.generic import NavigationListView

class ItemView(NavigationListView):
    def get_queryset(self):
        queryset = super(NavigationListView, self).get_queryset()

        # Need to filter by specific ID
        return queryset.filter(pk=self.kwargs["pk"])

