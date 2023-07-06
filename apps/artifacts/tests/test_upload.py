from os.path import isfile, join
from pathlib import Path
from shutil import rmtree

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from ..models import Artifact

from library.testing.const import TESTING_ASSETS


class UploadTestCase(TestCase):
    def test_default_directory(self):
        with open(join(TESTING_ASSETS, 'text.txt'), 'rb') as input_file:
            att = Artifact.objects.create(
                category=Artifact.RECEIPT,
                file=SimpleUploadedFile('text.txt', input_file.read())
            )

        self.assertEqual(Artifact.RECEIPT, att.category)
        self.assertEqual('', att.directory)
        self.assertEqual('upload/0000000001.txt', att.file.name)
        self.assertEqual('text.txt', att.original_filename)

        self.assertTrue(isfile(join(settings.BASE_DIR, att.file.name)))

    def test_specified_directory(self):
        with open(join(TESTING_ASSETS, 'text.txt'), 'rb') as input_file:
            att = Artifact.objects.create(
                directory='__unit_test',
                file=SimpleUploadedFile('text.txt', input_file.read())
            )

        self.assertEqual('', att.category)
        self.assertEqual('__unit_test', att.directory)
        self.assertEqual('upload/__unit_test/0000000001.txt', att.file.name)
        self.assertEqual('text.txt', att.original_filename)

        self.assertTrue(isfile(join(settings.BASE_DIR, att.file.name)))

    def tearDown(self) -> None:
        Path(join(settings.BASE_DIR, 'upload', '0000000001.txt')).unlink(missing_ok=True)
        try:
            rmtree(join(settings.BASE_DIR, 'upload', '__unit_test'))
        except FileNotFoundError:
            pass

