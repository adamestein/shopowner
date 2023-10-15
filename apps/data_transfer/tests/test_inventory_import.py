from decimal import Decimal
from os.path import join
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from ..import_data.inventory import ImportView, TAB_NAME

from inventory.models import Inventory

from library.testing.cbv import setup_view
from library.testing.const import TESTING_ASSETS

from vendors.models import Vendor


@patch('data_transfer.import_data.inventory.success')
class ImportInventoryTestCase(TestCase):
    fixtures = [
        'fixtures/testing/users.json'
    ]

    def setUp(self) -> None:
        self.data_dir = join(TESTING_ASSETS, 'data')
        self.user = User.objects.get(username='adam')

    def test_import_csv(self, mock_success):
        # First import, all inventory items will be new

        with open(join(self.data_dir, 'inventory1.csv'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        response.client = Client()      # Needed for assertRedirects()
        self.assertRedirects(response, reverse('data_transfer:import_inventory'), target_status_code=302)

        self._check_data1(mock_success)

        # Second import, some inventory items are the same which should increase the bought quantity

        with open(join(self.data_dir, 'inventory2.csv')) as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        response.client = Client()  # Needed for assertRedirects()
        self.assertRedirects(response, reverse('data_transfer:import_inventory'), target_status_code=302)
        
        self._check_data2(mock_success)

    def test_bad_header_csv(self, mock_success):
        with open(join(self.data_dir, 'bad_inventory_header.csv'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        self.assertEqual(
            'Header mismatch for "bad_inventory_header.csv"',
            response.context_data['form'].errors['file'].data[0].message.args[0]
        )

        self.assertEqual(0, mock_success.call_count)

    def test_import_ods(self, mock_success):
        # First import, all inventory items will be new

        with open(join(self.data_dir, 'data1.ods'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        response.client = Client()  # Needed for assertRedirects()
        self.assertRedirects(response, reverse('data_transfer:import_inventory'), target_status_code=302)

        self._check_data1(mock_success)

        # Second import, some inventory items are the same which should increase the bought quantity

        with open(join(self.data_dir, 'inventory2.csv')) as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        response.client = Client()  # Needed for assertRedirects()
        self.assertRedirects(response, reverse('data_transfer:import_inventory'), target_status_code=302)

        self._check_data2(mock_success)

    def test_no_inventory_tab_ods(self, mock_success):
        with open(join(self.data_dir, 'missing_tabs.ods'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        self.assertEqual(
            f'{TAB_NAME} tab not found in "missing_tabs.ods"',
            response.context_data['form'].errors['file'].data[0].message.args[0]
        )

        self.assertEqual(0, mock_success.call_count)

    def test_bad_header_ods(self, mock_success):
        with open(join(self.data_dir, 'bad_inventory_header.ods'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        self.assertEqual(
            f'Header mismatch for "bad_inventory_header.ods" on the {TAB_NAME} tab',
            response.context_data['form'].errors['file'].data[0].message.args[0]
        )

        self.assertEqual(0, mock_success.call_count)

    def test_missing_data(self, mock_success):
        # Not all fields are filled in

        with open(join(self.data_dir, 'missing_inventory_data.ods'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        response.client = Client()  # Needed for assertRedirects()
        self.assertRedirects(response, reverse('data_transfer:import_inventory'), target_status_code=302)

        inventory = Inventory.objects.all()
        self.assertEqual(4, inventory.count())

        self.assertEqual('Added Inventory – Tinte', inventory[0].label)
        self.assertEqual('', inventory[0].notes)
        self.assertEqual('', inventory[0].product_number)
        self.assertEqual(0, inventory[0].qty_bought)
        self.assertEqual(0, inventory[0].qty_sold)
        self.assertEqual(0, inventory[0].remaining)
        self.assertEqual('', inventory[0].stock_number)
        self.assertEqual(self.user, inventory[0].user)
        self.assertIsNone(inventory[0].vendor)
        self.assertEqual(Decimal('0'), inventory[0].wholesale_price)

        self.assertEqual('Grape Potion (orig sample)', inventory[1].label)
        self.assertEqual('', inventory[1].notes)
        self.assertEqual('', inventory[1].product_number)
        self.assertEqual(1, inventory[1].qty_bought)
        self.assertEqual(0, inventory[1].qty_sold)
        self.assertEqual(1, inventory[1].remaining)
        self.assertEqual('', inventory[1].stock_number)
        self.assertEqual(self.user, inventory[1].user)
        self.assertIsNone(inventory[1].vendor)
        self.assertEqual(Decimal('0'), inventory[1].wholesale_price)

        self.assertEqual('Peace Hand - Gold', inventory[2].label)
        self.assertEqual('', inventory[2].notes)
        self.assertEqual('Go-1046-G', inventory[2].product_number)
        self.assertEqual(6, inventory[2].qty_bought)
        self.assertEqual(0, inventory[2].qty_sold)
        self.assertEqual(6, inventory[2].remaining)
        self.assertEqual('ORN', inventory[2].stock_number)
        self.assertEqual(self.user, inventory[2].user)
        self.assertEqual(Vendor.objects.get(name='Cody Foster'), inventory[2].vendor)
        self.assertEqual(Decimal('8.35'), inventory[2].wholesale_price)

        self.assertEqual('Soul Flower Journals', inventory[3].label)
        self.assertEqual('', inventory[3].notes)
        self.assertEqual('', inventory[3].product_number)
        self.assertEqual(0, inventory[3].qty_bought)
        self.assertEqual(0, inventory[3].qty_sold)
        self.assertEqual(0, inventory[3].remaining)
        self.assertEqual('', inventory[3].stock_number)
        self.assertEqual(self.user, inventory[3].user)
        self.assertIsNone(inventory[3].vendor)
        self.assertEqual(Decimal('7.33'), inventory[3].wholesale_price)

        self.assertEqual(1, Vendor.objects.all().count())

        self.assertEqual(1, mock_success.call_count)
        self.assertEqual('Successfully imported 4 items into your inventory', mock_success.call_args_list[0][0][1])

    def _check_data1(self, mock_success):
        inventory = Inventory.objects.all()
        self.assertEqual(4, inventory.count())

        self.assertEqual('Cosmic Mushroom', inventory[0].label)
        self.assertEqual('', inventory[0].notes)
        self.assertEqual('Go-2899', inventory[0].product_number)
        self.assertEqual(6, inventory[0].qty_bought)
        self.assertEqual(0, inventory[0].qty_sold)
        self.assertEqual(6, inventory[0].remaining)
        self.assertEqual('ORN', inventory[0].stock_number)
        self.assertEqual(self.user, inventory[0].user)
        self.assertEqual(Vendor.objects.get(name='Cody Foster'), inventory[0].vendor)
        self.assertEqual(Decimal('7.30'), inventory[0].wholesale_price)

        self.assertEqual('Minecraft (MC)', inventory[1].label)
        self.assertEqual('*1 gift to Dante', inventory[1].notes)
        self.assertEqual('', inventory[1].product_number)
        self.assertEqual(10, inventory[1].qty_bought)
        self.assertEqual(9, inventory[1].qty_sold)
        self.assertEqual(1, inventory[1].remaining)
        self.assertEqual('', inventory[1].stock_number)
        self.assertEqual(self.user, inventory[1].user)
        self.assertEqual(Vendor.objects.get(name='Insanely Paracord'), inventory[1].vendor)
        self.assertEqual(Decimal('4.00'), inventory[1].wholesale_price)

        self.assertEqual('Rainbow Wrap Llama', inventory[2].label)
        self.assertEqual('', inventory[2].notes)
        self.assertEqual('486003000', inventory[2].product_number)
        self.assertEqual(2, inventory[2].qty_bought)
        self.assertEqual(0, inventory[2].qty_sold)
        self.assertEqual(2, inventory[2].remaining)
        self.assertEqual('', inventory[2].stock_number)
        self.assertEqual(self.user, inventory[2].user)
        self.assertEqual(Vendor.objects.get(name='DZI Handmade'), inventory[2].vendor)
        self.assertEqual(Decimal('12.50'), inventory[2].wholesale_price)

        self.assertEqual('Tits Mug', inventory[3].label)
        self.assertEqual('', inventory[3].notes)
        self.assertEqual('MG01-SEI', inventory[3].product_number)
        self.assertEqual(4, inventory[3].qty_bought)
        self.assertEqual(0, inventory[3].qty_sold)
        self.assertEqual(4, inventory[3].remaining)
        self.assertEqual('', inventory[3].stock_number)
        self.assertEqual(self.user, inventory[3].user)
        self.assertEqual(Vendor.objects.get(name='Sarah Edmond'), inventory[3].vendor)
        self.assertEqual(Decimal('1.60'), inventory[3].wholesale_price)

        self.assertEqual(4, Vendor.objects.all().count())

        self.assertEqual(1, mock_success.call_count)
        self.assertEqual('Successfully imported 4 items into your inventory', mock_success.call_args_list[0][0][1])

    def _check_data2(self, mock_success):

        inventory = Inventory.objects.all()
        self.assertEqual(6, inventory.count())

        self.assertEqual('Boobies Mug', inventory[0].label)
        self.assertEqual('', inventory[0].notes)
        self.assertEqual('MG02-SEI', inventory[0].product_number)
        self.assertEqual(3, inventory[0].qty_bought)
        self.assertEqual(0, inventory[0].qty_sold)
        self.assertEqual(3, inventory[0].remaining)
        self.assertEqual('', inventory[0].stock_number)
        self.assertEqual(self.user, inventory[0].user)
        self.assertEqual(Vendor.objects.get(name='Sarah Edmond'), inventory[0].vendor)
        self.assertEqual(Decimal('2.13'), inventory[0].wholesale_price)

        self.assertEqual('Cosmic Mushroom', inventory[1].label)
        self.assertEqual('', inventory[1].notes)
        self.assertEqual('Go-2899', inventory[1].product_number)
        self.assertEqual(6, inventory[1].qty_bought)
        self.assertEqual(0, inventory[1].qty_sold)
        self.assertEqual(6, inventory[1].remaining)
        self.assertEqual('ORN', inventory[1].stock_number)
        self.assertEqual(self.user, inventory[1].user)
        self.assertEqual(Vendor.objects.get(name='Cody Foster'), inventory[1].vendor)
        self.assertEqual(Decimal('7.30'), inventory[1].wholesale_price)

        self.assertEqual('Ginger Bread Yoga', inventory[2].label)
        self.assertEqual('', inventory[2].notes)
        self.assertEqual('Go-6696', inventory[2].product_number)
        self.assertEqual(6, inventory[2].qty_bought)
        self.assertEqual(0, inventory[2].qty_sold)
        self.assertEqual(6, inventory[2].remaining)
        self.assertEqual('ORN', inventory[2].stock_number)
        self.assertEqual(self.user, inventory[2].user)
        self.assertEqual(Vendor.objects.get(name='Cody Foster'), inventory[2].vendor)
        self.assertEqual(Decimal('7.92'), inventory[2].wholesale_price)

        self.assertEqual('Minecraft (MC)', inventory[3].label)
        self.assertEqual('*1 gift to Dante\n*1 gift to Dante', inventory[3].notes)
        self.assertEqual('', inventory[3].product_number)
        self.assertEqual(29, inventory[3].qty_bought)
        self.assertEqual(9, inventory[3].qty_sold)
        self.assertEqual(20, inventory[3].remaining)
        self.assertEqual('', inventory[3].stock_number)
        self.assertEqual(self.user, inventory[3].user)
        self.assertEqual(Vendor.objects.get(name='Insanely Paracord'), inventory[3].vendor)
        self.assertEqual(Decimal('4.00'), inventory[3].wholesale_price)

        self.assertEqual('Rainbow Wrap Llama', inventory[4].label)
        self.assertEqual('', inventory[4].notes)
        self.assertEqual('486003000', inventory[4].product_number)
        self.assertEqual(4, inventory[4].qty_bought)
        self.assertEqual(0, inventory[4].qty_sold)
        self.assertEqual(4, inventory[4].remaining)
        self.assertEqual('', inventory[4].stock_number)
        self.assertEqual(self.user, inventory[4].user)
        self.assertEqual(Vendor.objects.get(name='DZI Handmade'), inventory[4].vendor)
        self.assertEqual(Decimal('12.50'), inventory[4].wholesale_price)

        self.assertEqual('Tits Mug', inventory[5].label)
        self.assertEqual('', inventory[5].notes)
        self.assertEqual('MG01-SEI', inventory[5].product_number)
        self.assertEqual(4, inventory[5].qty_bought)
        self.assertEqual(0, inventory[5].qty_sold)
        self.assertEqual(4, inventory[5].remaining)
        self.assertEqual('', inventory[5].stock_number)
        self.assertEqual(self.user, inventory[5].user)
        self.assertEqual(Vendor.objects.get(name='Sarah Edmond'), inventory[5].vendor)
        self.assertEqual(Decimal('1.60'), inventory[5].wholesale_price)

        self.assertEqual(4, Vendor.objects.all().count())

        self.assertEqual(2, mock_success.call_count)
        self.assertEqual('Successfully imported 4 items into your inventory', mock_success.call_args_list[1][0][1])
