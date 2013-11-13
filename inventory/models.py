from db_file_storage.model_utils import delete_file_if_needed
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

    picture = models.ImageField(
        upload_to="inventory.ItemImage/data/filename/mimetype",
        blank=True,
        null=True,
        help_text = "Item image",
    )

    # Move to a sales table
    #discount = models.FloatField(
    #    default = 0,
    #    help_text = "Price discount at time of sale (in percentage)"
    #)

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

    comments = models.TextField(
        blank = True,
    )

    remove = models.BooleanField(
        default = False,
        help_text = "Check to remove this item from inventory (and not because it was sold)"
    )

    class Meta:
        ordering = ("number",)
        unique_together = (("user", "number"),)

    def save(self, *args, **kwargs):
        delete_file_if_needed(self, "picture")
        super(Item, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.number + ": " + self.desc + " (%s)" % currency(self.price)

# Image of the item
class ItemImage(models.Model):
    data = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)

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
        help_text = "Check to remove this seller",
    )

    class Meta:
        ordering = ("last_name", "first_name")
        unique_together = (("first_name", "last_name"),)

    def __unicode__(self):
        return self.last_name + ", " + self.first_name

