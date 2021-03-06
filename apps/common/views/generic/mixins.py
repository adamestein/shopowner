import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin, ModelFormMixin


class NavigationContextMixin(ContextMixin):
    navigation = None

    # noinspection PyUnresolvedReferences
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(NavigationContextMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(NavigationContextMixin, self).get_context_data(**kwargs)

        # Add web page navigation and version info
        context["navigation"] = self.navigation

        return context


# noinspection PyUnresolvedReferences
class NavigationEditMixin(NavigationContextMixin, ModelFormMixin):
    action = None

    def form_valid(self, form):
        # Add the message if we have one
        if hasattr(self, "message") and self.message is not None:
                messages.add_message(self.request, messages.INFO, self.message)

        return super(NavigationEditMixin, self).form_valid(form)

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


# noinspection PyUnresolvedReferences
class PopupAddMixin(FormMixin):
    # noinspection PyProtectedMember
    def form_valid(self, form):
        try:
            saved_object = form.save()
        except IntegrityError:
            saved_object = None

        # Need to return the JavaScript that will close the popup window
        if saved_object and "_popup" in self.request.GET:
            return HttpResponse(
                '<script type="text/javascript">opener.dismissAddAnotherPopup(window, "%s", "%s");</script>' %
                (escape(saved_object._get_pk_val()), escape(saved_object)))

        return super(PopupAddMixin, self).form_valid(form)

    # noinspection PyPep8Naming
    def form_invalid(self, form):
        if "_popup" in self.request.GET:
            # Add the _popup field to POST so that we continue using the correct template
            post_values = self.request.POST.copy()
            post_values["_popup"] = True
            self.request.POST = post_values

        return super(PopupAddMixin, self).form_invalid(form)

    # noinspection PyAttributeOutsideInit
    def get_context_data(self, **kwargs):
        # Both GET and POST requests pass through here, so we are using this
        # focal point to determine if we need to switch templates to the
        # "popup" version.
        #
        # Also, the form_invalid() method ultimately renders the form calling
        # get_context_data() so we have an opportunity to change the template
        # being used before being rendered.
        if "_popup" in self.request.GET or "_popup" in self.request.POST:
            # Change the name to get a suitable popup version of the form
            name = os.path.splitext(self.template_name)
            self.template_name = name[0] + "_popup" + name[1]

        # Call the base implementation first to get a context
        context = super(PopupAddMixin, self).get_context_data(**kwargs)

        return context

