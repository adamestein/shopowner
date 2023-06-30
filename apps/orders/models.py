from os.path import join

from django.db import models

from vendors.models import Vendor


def update_receipt_filename(instance, filename):
    # Change the saved receipt file to contain the database row ID of the order to make the filename distinct
    _, _, extension = filename.rpartition('.')
    return f'{join("upload", "receipts", str(instance.id).zfill(10) + "." + extension)}'


class Order(models.Model):
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

    date_ordered = models.DateField(help_text='Date when order was placed')

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

    receipt = models.FileField(
        blank=True,
        help_text='Receipt file (leave empty for hardcopy)',
        null=True,
        upload_to=update_receipt_filename
    )

    notes = models.TextField(
        blank=True,
        help_text='Any miscellaneous information can go here'
    )

    class Meta:
        ordering = ('vendor', 'reference_number')

    def save(self, *args, **kwargs):
        # Need to save the instance without a receipt file first so there is a database row ID that can be added
        # to the uploaded filename
        if self.pk is None:
            receipt = self.receipt
            self.receipt = None
            super().save(*args, **kwargs)
            self.receipt = receipt

        super().save(*args, **kwargs)

    def __str__(self):
        return f'[{self.vendor.name}] {self.reference_number}'


class PaymentMethod(models.Model):
    label = models.TextField(help_text='Method of payment', max_length=30)

    class Meta:
        ordering = ('label', )

    def __str__(self):
        return self.label
