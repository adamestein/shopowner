from django.core import serializers
from django.db.models import Q

from common.views.generic import AJAXView, NavigationListView
from models import Category, Item, Seller


class ItemListView(NavigationListView):
    # noinspection PyUnresolvedReferences
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ItemListView, self).get_context_data(**kwargs)

        # Add the categories and sellers for the search form
        context["categories"] = Category.objects.filter(user=self.request.user)
        context["sellers"] = Seller.objects.filter(user=self.request.user)

        return context


class ItemView(ItemListView):
    def get_queryset(self):
        queryset = super(ItemView, self).get_queryset()

        # Need to filter by specific ID
        # noinspection PyUnresolvedReferences
        return queryset.filter(pk=self.kwargs["pk"])


class SearchView(AJAXView):
    # noinspection PyUnresolvedReferences
    def get_context_data(self, **kwargs):
        number = self.request.GET["number"]
        desc = self.request.GET["desc"]
        categories = self.request.GET.getlist("categories[]")
        sellers = self.request.GET.getlist("sellers[]")

        query = Q(user=self.request.user)

        if number != "":
            query &= Q(number=number)

        if desc != "":
            query &= Q(desc__icontains=desc)

        if len(categories):
            query &= Q(category__in=categories)

        if len(sellers):
            query &= Q(sellers__id__in=sellers)

        sold = []
        for item in Item.objects.filter(query):
            if item.sale_set.all():
                sold.append(item.pk)

        return {
            "list": serializers.serialize("json", Item.objects.filter(query)),
            "sold": sold
        }