from os.path import join
import pathlib

from django.conf import settings
from django.db import models
from django.db.utils import IntegrityError


def update_filename(instance, filename):
    # Change the saved file to contain the database row ID of the artifact to make the filename distinct. Also, store
    # the original name.
    instance.original_filename = filename
    ext = pathlib.Path(filename).suffix
    return f'{join("upload", instance.directory, str(instance.id).zfill(10) + ext.lower())}'


class Artifact(models.Model):
    # Categories
    RECEIPT = 'receipt'

    CATEGORY_CHOICES = (
        (RECEIPT, 'Receipt'),
    )

    category = models.CharField(
        choices=CATEGORY_CHOICES,
        help_text='Artifact category',
        max_length=7
    )

    directory = models.CharField(
        blank=True,
        help_text=f'Relative directory from {settings.BASE_DIR}/upload which is the default',
        max_length=50
    )

    original_filename = models.CharField(
        help_text='Name of uploaded file',
        max_length=200
    )

    file = models.FileField(
        blank=True,
        help_text='Uploaded file',
        null=True,
        upload_to=update_filename
    )

    class Meta:
        ordering = ('original_filename', )

    def save(self, *args, **kwargs):
        # Need to save the instance without an uploaded file first so there is a database row ID that can be added
        # to the uploaded filename
        if self.pk is None:
            original_file = self.file
            self.file = None
            super().save(*args, **kwargs)
            if original_file:
                self.file = original_file

                try:
                    # This 2nd call to super() with an uploaded file is needed for Django Admin but causes a
                    # database integrity error when using Attachments.objects.create().
                    super().save(*args, **kwargs)
                except IntegrityError:
                    pass
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.original_filename} ({self.file})'
