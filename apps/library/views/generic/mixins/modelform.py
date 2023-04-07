from django.contrib.messages import success
from django.views.generic.edit import ModelFormMixin


class AppModelFormMixin(ModelFormMixin):
    action = None
    success_message = None

    def form_valid(self, form):
        # noinspection PyAttributeOutsideInit
        self.object = form.save(commit=False)
        # noinspection PyUnresolvedReferences
        self.object.user = self.request.user        # Doesn't matter if updating as it's the same value
        self.object.save()

        if self.success_message:
            self.success_message = self.success_message % form.cleaned_data

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = self.action
        return context

    def get_success_url(self):
        if self.success_message:
            # noinspection PyUnresolvedReferences
            success(self.request, self.success_message)

        return super().get_success_url()
