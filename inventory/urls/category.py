from django.core.urlresolvers import reverse_lazy
from django.conf.urls import patterns, url

from common.views.generic import *

from ..forms import CategoryForm, CategoryEditForm, CategoryEditListForm
from ..models import Category
from ..navigation import navigation

urlpatterns = patterns(
    'category',

    url(
        r'^add/$',
        NavigationCreateView.as_view(
            action="Add",
            form_class=CategoryForm,
            navigation=navigation("add_category"),
            success_url=reverse_lazy("category_add"),
            template_name="category_form.html",
            message="<em>Category List</em> has been updated"
        ),
        name="category_add"
    ),

    url(
        r'^edit/$',
        NavigationFormView.as_view(
            form_class=CategoryEditListForm,
            navigation=navigation("edit_category"),
            template_name="category_edit_list.html"
        )
    ),

    url(
        r'^edit/(?P<pk>[\d]+)$',
        NavigationUpdateView.as_view(
            form_class=CategoryEditForm,
            model=Category,
            navigation=navigation("edit_category"),
            success_url="../updated/",
            template_name="category_form.html"
        ),
        name="edit_specific_category"
    ),

    url(
        r'^list/$',
        NavigationListView.as_view(
            model=Category,
            navigation=navigation("list_categories"),
            queryset=Category.objects.filter(remove=False),
            template_name="category_list.html"
        )
    ),

    url(
        r'^updated/$',
        NavigationTemplateView.as_view(
            navigation=navigation(""),
            template_name="category_updated.html"
        )
    ),
)