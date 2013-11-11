from django.contrib.auth.models import User
from django.db import models

from common.format import currency

# Item being kept track off
class Item(models.Model):
    user = models.ForeignKey(User,
        help_text = "User account this item belongs to",
    )

    number = models.CharField(
        max_length = 5,
        help_text = "Item number",
    )

    desc = models.CharField(
        max_length = 100,
        help_text = "Description of the item",
    )

    owner = models.ManyToManyField("Seller",
        help_text = "Seller(s) of this item",
    )

    price = models.DecimalField(
        decimal_places = 2,
        max_digits = 10,
        help_text = "Price of the item",
    )

    picture = models.URLField(
        blank = True,
        null = True,
        help_text = "URL to the full-sized image of the item",
    )

    discount = models.FloatField(
        default = 0,
        help_text = "Price discount at time of sale (in percentage)"
    )

    # Move to a sales table
    #sale_price = models.DecimalField(
    #    decimal_places = 2,
    #    max_digits = 10,
    #    blank = True,
    #    null = True,
    #    help_text = "Price the item sold for",
    #)
#
#    sale_date = models.DateField(
#        db_index = True,
#        blank = True,
#        null = True,
#        help_text = "Date on which the item sold",
#    )

    remove = models.BooleanField(
        default = False,
        help_text = "Set to remove this item from inventory (and not because it was sold)"
    )

    comments = models.TextField(
        blank = True,
    )

    class Meta:
        ordering = ("number",)
        unique_together = (("user", "number"),)

    def __unicode__(self):
        return self.number + ": " + self.desc + " (%s)" % currency(self.price)

# Owner selling the item
class Seller(models.Model):
    first_name = models.CharField(
        max_length = 20,
    )

    last_name = models.CharField(
        max_length = 20,
    )

    remove = models.BooleanField(
        default = False,
        help_text = "Set to remove this seller",
    )

    class Meta:
        ordering = ("last_name", "first_name")
        unique_together = (("first_name", "last_name"),)

    def __unicode__(self):
        return self.last_name + ", " + self.first_name

