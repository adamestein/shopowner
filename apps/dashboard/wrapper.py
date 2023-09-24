from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import RedirectView


# Since the dashboard is set up with permissions for authenticated users only, can't have '/' automatically redirect
# there as it just returns 403 Forbidden rather than going to the login page if the user isn't logged in. Therefore,
# we put a wrapper in place that will go the login screen when needed before going onto the dashboard page.
class Wrapper(LoginRequiredMixin, RedirectView):
    pattern_name = 'dashboard'
