from django.db import models


class Vendor(models.Model):
    name = models.CharField(
        help_text="Vendor's name",
        max_length=50
    )

    website = models.URLField(
        blank=True,
        help_text="Vendor's website",
        null=True
    )

    running_investment = models.DecimalField(
        decimal_places=2,
        default=0,
        help_text='Total amount spent with this vendor',
        max_digits=10,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
