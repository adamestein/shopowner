# noinspection PyPackageRequirements
from localflavor.us.models import USStateField

from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.dateformat import DateFormat

from common.format import currency
from inventory.models import Item


class Sale(models.Model):
    user = models.ForeignKey(
        User,
        help_text="User account this information belongs to",
    )

    item = models.ForeignKey(
        Item,
        help_text="Item which was sold"
    )

    tax_rate = models.FloatField(
        help_text="Tax rate at time of sale (in percentage)",
    )

    discount = models.FloatField(
        default=0,
        help_text="Price discount at time of sale (in percentage)"
    )

    price = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        help_text="Price the item sold for (includes sales tax)",
    )

    qty = models.PositiveIntegerField(
        default=1,
        help_text='How many were sold',
        validators=[MinValueValidator(1)]
    )

    commission = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        blank=True,
        null=True,
        help_text="Commission made on this item",
    )

    date = models.DateField(
        db_index=True,
        blank=True,   # Temporary until Gina gets her "sold" data in, then we can go back to date is required
        null=True,
        help_text="Date on which the item sold",
    )

    class Meta:
        ordering = ("item__sku", "date", "item__desc")
        unique_together = ("item", "user")

    def __str__(self):
        formatted_text = "'%s' sold for %s" % (self.item.desc, currency(self.price))

        if self.date:
            formatted_text += " on %s" % DateFormat(self.date).format("m/d/Y")

        return formatted_text


class Tax(models.Model):
    county = models.CharField(
        max_length=50,
    )

    state = USStateField()

    sales_tax = models.FloatField(help_text='Current tax rate (in percentage)')

    class Meta:
        ordering = ("state", "county")
        verbose_name_plural = "Taxes"
        unique_together = ("county", "state")

    def __str__(self):
        return "%s, %s County = %0.2f%%" % (self.state, self.county, float(self.sales_tax))

