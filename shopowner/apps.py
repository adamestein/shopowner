from django.apps import AppConfig
from django.conf.global_settings import AUTH_USER_MODEL
from django.db.models.signals import post_save


class ShopOwnerAppConfig(AppConfig):
    name = 'shopowner'

    def ready(self):
        # Every time a new user is created, add them to the 'Use Add Popup Form' group so that they can use the popup
        # form to add vendors, receipts, etc.
        post_save.connect(add_to_default_group, sender=AUTH_USER_MODEL)


# noinspection PyUnusedLocal
def add_to_default_group(sender, **kwargs):
    from django.contrib.auth.models import Group

    user = kwargs['instance']
    if kwargs['created']:
        group = Group.objects.get(name='Use Add Popup Form')
        user.groups.add(group)
