from django.contrib.auth.models import User
from django.db import models
from django.utils.dateformat import DateFormat
from localflavor.us.models import USStateField

from common.format import currency
from inventory.models import Item

from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^localflavor\.us\.models\.USStateField"])

class Sale(models.Model):
    user = models.ForeignKey(User,
        help_text = "User account this information belongs to",
    )

    item = models.ForeignKey(Item,
        help_text = "Item which was sold"
    )

    tax_rate = models.FloatField(
        help_text = "Tax rate at time of sale (in percentage)",
    )

    discount = models.FloatField(
        default = 0,
        help_text = "Price discount at time of sale (in percentage)"
    )

    price = models.DecimalField(
        decimal_places = 2,
        max_digits = 10,
        help_text = "Price the item sold for",
    )

    date = models.DateField(
        db_index = True,
        help_text = "Date on which the item sold",
    )

    class Meta:
        ordering = ("date", "item__desc")
        unique_together = ("item", "user")

    def __unicode__(self):
        return "'%s' sold for %s on %s" % \
                (self.item.desc, currency(self.price), DateFormat(self.date).format("m/d/Y"))

class Tax(models.Model):
    county = models.CharField(
        max_length = 50,
    )

    state = USStateField()

    sales_tax = models.FloatField(
        help_text = "Current tax rate (in percentage)",
    )

    class Meta:
        ordering = ("state", "county")
        verbose_name_plural = "Taxes"
        unique_together = ("county", "state")

    def __unicode__(self):
        return "%s, %s County = %0.2f%%" % (self.state, self.county, self.sales_tax)

