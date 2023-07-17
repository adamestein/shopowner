from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from artifacts.models import Artifact
from inventory.models import Inventory

from vendors.models import Vendor


class Item(models.Model):
    item = models.ForeignKey(Inventory)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        ordering = ('order', 'item')
        unique_together = ('order', 'item')

    def __str__(self):
        return f'{self.item} <--> {self.order}'


class Order(models.Model):
    deleted = models.BooleanField(default=False, help_text='Delete this order from the database')

    user = models.ForeignKey(
        User,
        help_text="User account this order belongs to"
    )

    reference_number = models.CharField(
        blank=True,
        help_text='Order number/reference number',
        max_length=20,
        null=True
    )

    vendor = models.ForeignKey(
        Vendor,
        help_text='Vendor this order was purchased from'
    )

    items = models.ManyToManyField(
        Inventory,
        help_text='Items bought in this order',
        through=Item
    )

    date_ordered = models.DateField(
        blank=True,
        help_text='Date when order was placed',
        null=True
    )

    date_received = models.DateField(
        blank=True,
        help_text='Date when order was received',
        null=True
    )

    net_cost = models.DecimalField(
        decimal_places=2,
        help_text='Net cost for the order',
        max_digits=10,
    )

    shipping_cost = models.DecimalField(
        decimal_places=2,
        default=0,
        help_text='Tax credit paid for the order',
        max_digits=10,
    )

    tax = models.DecimalField(
        decimal_places=2,
        default=0,
        help_text='Tax credit paid for the order',
        max_digits=10,
    )

    payment_method = models.ForeignKey(
        'PaymentMethod',
        blank=True,
        help_text='Method of payment for this order',
        null=True
    )

    receipts = models.ManyToManyField(
        Artifact,
        blank=True,
        help_text='Uploaded receipt documents associated with this order'
    )

    notes = models.TextField(
        blank=True,
        help_text='Any miscellaneous information can go here'
    )

    class Meta:
        ordering = ('date_ordered', 'date_received', 'vendor', 'reference_number')

    @property
    def total_cost(self):
        return self.net_cost + self.shipping_cost

    def __str__(self):
        return f'[{self.vendor.name}] {self.reference_number}'


class PaymentMethod(models.Model):
    label = models.CharField(
        help_text='Method of payment',
        max_length=30,
        unique=True
    )

    class Meta:
        ordering = ('label', )

    def __str__(self):
        return self.label
