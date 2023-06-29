from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Inventory(models.Model):
    deleted = models.BooleanField(default=False, help_text='Delete this item from inventory')

    label = models.CharField(
        help_text="Item label for display",
        max_length=100
    )

    notes = models.TextField(help_text='Any miscellaneous information can go here')

    qty_bought = models.PositiveIntegerField(
        help_text='Quantity of this item purchased',
        validators=[MinValueValidator(1)]
    )

    qty_sold = models.PositiveIntegerField(
        default=0,
        help_text='Quantity of this item sold'
    )

    product_number = models.CharField(
        help_text="Vendor's product number for this item",
        max_length=50,
    )

    stock_number = models.CharField(
        help_text="My stock number for this item",
        max_length=50,
    )

    wholesale_price = models.DecimalField(
        decimal_places=2,
        help_text='Wholesale price per item unit',
        max_digits=10,
    )

    user = models.ForeignKey(
        User,
        help_text="User account this item belongs to"
    )

    vendor = models.ForeignKey(
        'Vendor',
        blank=True,
        help_text='Vendor this item was purchased from',
        null=True
    )

    class Meta:
        ordering = ('label',)
        unique_together = ('label', 'product_number', 'stock_number', 'user', 'vendor')
        verbose_name_plural = 'Inventories'

    def price_per_unit(self, total_cost):
        return total_cost / self.qty_bought

    @property
    def remaining(self):
        return self.qty_bought - self.qty_sold

    def __str__(self):
        return self.label


class Vendor(models.Model):
    name = models.CharField(
        help_text="Vendor's name",
        max_length=50
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
