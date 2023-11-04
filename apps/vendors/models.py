from django.db import models


class Vendor(models.Model):
    name = models.CharField(
        help_text="Vendor's name",
        max_length=50,
        unique=True
    )

    website = models.URLField(
        blank=True,
        help_text="Vendor's website",
        null=True
    )

    class Meta:
        ordering = ('name',)

    @property
    def running_investment(self):
        return sum([order.total_cost for order in self.order_set.all()])

    def __str__(self):
        return self.name
