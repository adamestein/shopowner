from django.contrib.auth.models import User
from django.db import models

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
        editable = False,
        blank = True,
        null = True,
    )

    discount = models.FloatField(
        default = 0,
        help_text = "Price discount at time of sale (in percentage)"
    )

    sale_price = models.DecimalField(
        decimal_places = 2,
        max_digits = 10,
        blank = True,
        null = True,
        help_text = "Price the item sold for",
    )

    sale_date = models.DateField(
        db_index = True,
        blank = True,
        null = True,
        help_text = "Date on which the item sold",
    )

    removed = models.BooleanField(
        default = False,
        help_text = "Set to indicate item was removed and not because it was sold",
    )

    class Meta:
        unique_together = (("user", "number"),)

class Seller(models.Model):
    first_name = models.CharField(
        max_length = 20,
    )

    last_name = models.CharField(
        max_length = 20,
    )

