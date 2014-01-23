from django.views.generic import CreateView, FormView, UpdateView

from mixins import PopupAddMixin, NavigationContextMixin, NavigationEditMixin

class NavigationCreateView(PopupAddMixin, NavigationEditMixin, CreateView):
    action = "Create"
    message = None

    def form_valid(self, form):
        # Will not cause a problem if form.instance.user doesn't exist beforehand
        form.instance.user = self.request.user

        return super(NavigationCreateView, self).form_valid(form)


class NavigationFormView(NavigationContextMixin, FormView):
    def get_form_kwargs(self):
        kwargs = super(NavigationFormView, self).get_form_kwargs()
        kwargs.update({"user": self.request.user})  # Add user so form can use value to filter

        return kwargs

class NavigationUpdateView(NavigationEditMixin, UpdateView):
    action = "Update"
    message = None