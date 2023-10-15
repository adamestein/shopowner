from datetime import date
from decimal import Decimal
from os.path import join
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from ..import_data.orders import ImportView, TAB_NAME

from library.testing.cbv import setup_view
from library.testing.const import TESTING_ASSETS

from orders.models import Order, PaymentMethod

from vendors.models import Vendor


@patch('data_transfer.import_data.orders.success')
class ImportOrdersTestCase(TestCase):
    fixtures = [
        'fixtures/testing/users.json'
    ]

    def setUp(self) -> None:
        self.data_dir = join(TESTING_ASSETS, 'data')
        self.user = User.objects.get(username='adam')

    def test_import_csv(self, mock_success):
        with open(join(self.data_dir, 'orders.csv'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        response.client = Client()  # Needed for assertRedirects()
        self.assertRedirects(response, reverse('data_transfer:import_orders'), target_status_code=302)

        self._check_data(mock_success)

        self._check_payment_methods()
        self._check_vendors()

    def test_bad_header_csv(self, mock_success):
        with open(join(self.data_dir, 'bad_order_header.csv'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        self.assertEqual(
            'Header mismatch for "bad_order_header.csv"',
            response.context_data['form'].errors['file'].data[0].message.args[0]
        )

        self.assertEqual(0, mock_success.call_count)

    def test_import_ods(self, mock_success):
        with open(join(self.data_dir, 'data1.ods'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        response.client = Client()  # Needed for assertRedirects()
        self.assertRedirects(response, reverse('data_transfer:import_orders'), target_status_code=302)

        self._check_data(mock_success)

        self._check_payment_methods()
        self._check_vendors()

    def test_no_orders_tab_ods(self, mock_success):
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
        with open(join(self.data_dir, 'bad_order_header.ods'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        self.assertEqual(
            f'Header mismatch for "bad_order_header.ods" on the {TAB_NAME} tab',
            response.context_data['form'].errors['file'].data[0].message.args[0]
        )

        self.assertEqual(0, mock_success.call_count)

    def test_missing_vendor_csv(self, mock_success):
        with open(join(self.data_dir, 'missing_vendor.csv'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        response.client = Client()  # Needed for assertRedirects()
        self.assertRedirects(response, reverse('data_transfer:import_orders'), target_status_code=302)

        self._check_data(mock_success, missing_vendor_test=True)

        self._check_payment_methods()
        self._check_vendors(missing_vendor_test=True)

    def test_missing_vendor_ods(self, mock_success):
        with open(join(self.data_dir, 'missing_vendor.ods'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        response.client = Client()  # Needed for assertRedirects()
        self.assertRedirects(response, reverse('data_transfer:import_orders'), target_status_code=302)

        self._check_data(mock_success, missing_vendor_test=True)

        self._check_payment_methods()
        self._check_vendors(missing_vendor_test=True)

    def test_missing_net_cost_csv(self, mock_success):
        with open(join(self.data_dir, 'missing_net_cost.csv'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        self.assertEqual(
            'Missing net cost in "missing_net_cost.csv" (line 11)',
            response.context_data['form'].errors['file'].data[0].message.args[0]
        )

        self.assertEqual(0, mock_success.call_count)

    def test_missing_net_cost_ods(self, mock_success):
        with open(join(self.data_dir, 'missing_net_cost.ods'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        self.assertEqual(
            'Missing net cost in "missing_net_cost.ods" (line 11)',
            response.context_data['form'].errors['file'].data[0].message.args[0]
        )

        self.assertEqual(0, mock_success.call_count)

    def test_bad_receiving_date_csv(self, mock_success):
        with open(join(self.data_dir, 'bad_receiving_date.csv'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        self.assertEqual(
            'Received date is BEFORE the order date in "bad_receiving_date.csv" (line 2)',
            response.context_data['form'].errors['file'].data[0].message.args[0]
        )

        self.assertEqual(0, mock_success.call_count)

    def test_bad_receiving_date_ods(self, mock_success):
        with open(join(self.data_dir, 'bad_receiving_date.ods'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        self.assertEqual(
            'Received date is BEFORE the order date in "bad_receiving_date.ods" (line 2)',
            response.context_data['form'].errors['file'].data[0].message.args[0]
        )

        self.assertEqual(0, mock_success.call_count)

    def _check_data(self, mock_success, missing_vendor_test=False):
        count = 15 if missing_vendor_test else 16

        orders = Order.objects.all()
        self.assertEqual(count, orders.count())

        self.assertIsNone(orders[0].date_ordered)
        self.assertEqual(date(2022, 5, 3), orders[0].date_received)
        self.assertEqual(0, orders[0].items.count())
        self.assertEqual(Decimal('225'), orders[0].net_cost)
        self.assertEqual('little keychains and pals\n\npicked up', orders[0].notes)
        self.assertIsNone(orders[0].payment_method)
        self.assertEqual(0, orders[0].receipts.count())
        self.assertEqual('#1721', orders[0].reference_number)
        self.assertEqual(Decimal('0'), orders[0].shipping_cost)
        self.assertEqual(Decimal('18'), orders[0].tax)
        self.assertEqual(Decimal('225'), orders[0].total_cost)
        self.assertEqual(self.user, orders[0].user)
        self.assertEqual(Vendor.objects.get(name='Insanely Paracord'), orders[0].vendor)

        self.assertIsNone(orders[1].date_ordered)
        self.assertEqual(date(2022, 5, 4), orders[1].date_received)
        self.assertEqual(0, orders[1].items.count())
        self.assertEqual(Decimal('30'), orders[1].net_cost)
        self.assertEqual('little keychains and pals\n\npicked up', orders[1].notes)
        self.assertIsNone(orders[1].payment_method)
        self.assertEqual(0, orders[1].receipts.count())
        self.assertEqual('#1724', orders[1].reference_number)
        self.assertEqual(Decimal('0'), orders[1].shipping_cost)
        self.assertEqual(Decimal('2.40'), orders[1].tax)
        self.assertEqual(Decimal('30'), orders[1].total_cost)
        self.assertEqual(self.user, orders[1].user)
        self.assertEqual(Vendor.objects.get(name='Insanely Paracord'), orders[1].vendor)

        self.assertEqual(date(2022, 3, 12), orders[2].date_ordered)
        self.assertIsNone(orders[2].date_received)
        self.assertEqual(0, orders[2].items.count())
        self.assertEqual(Decimal('128'), orders[2].net_cost)
        self.assertEqual('Fair Trade Items- Various Items', orders[2].notes)
        self.assertIsNone(orders[2].payment_method)
        self.assertEqual(0, orders[2].receipts.count())
        self.assertEqual('0039823', orders[2].reference_number)
        self.assertEqual(Decimal('24.29'), orders[2].shipping_cost)
        self.assertEqual(Decimal('0'), orders[2].tax)
        self.assertEqual(Decimal('152.29'), orders[2].total_cost)
        self.assertEqual(self.user, orders[2].user)
        self.assertEqual(Vendor.objects.get(name='Dzi Handmade'), orders[2].vendor)

        self.assertEqual(date(2022, 3, 14), orders[3].date_ordered)
        self.assertIsNone(orders[3].date_received)
        self.assertEqual(0, orders[3].items.count())
        self.assertEqual(Decimal('63.40'), orders[3].net_cost)
        self.assertEqual('Rose Buds, Chamomile Flowers and Lavender Flowers', orders[3].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Visa'), orders[3].payment_method)
        self.assertEqual(0, orders[3].receipts.count())
        self.assertEqual('1464787', orders[3].reference_number)
        self.assertEqual(Decimal('18.26'), orders[3].shipping_cost)
        self.assertEqual(Decimal('1.46'), orders[3].tax)
        self.assertEqual(Decimal('81.66'), orders[3].total_cost)
        self.assertEqual(self.user, orders[3].user)
        self.assertEqual(Vendor.objects.get(name='Starwest Botanicals'), orders[3].vendor)

        if missing_vendor_test:
            start_index = 4
        else:
            start_index = 5
            
            self.assertEqual(date(2022, 3, 15), orders[4].date_ordered)
            self.assertIsNone(orders[4].date_received)
            self.assertEqual(0, orders[4].items.count())
            self.assertEqual(Decimal('90'), orders[4].net_cost)
            self.assertEqual('Sunflower Chocolate for Ukraine\n\nFor donation', orders[4].notes)
            self.assertIsNone(orders[4].payment_method)
            self.assertEqual(0, orders[4].receipts.count())
            self.assertEqual('', orders[4].reference_number)
            self.assertEqual(Decimal('0'), orders[4].shipping_cost)
            self.assertEqual(Decimal('7.20'), orders[4].tax)
            self.assertEqual(Decimal('90'), orders[4].total_cost)
            self.assertEqual(self.user, orders[4].user)
            self.assertEqual(Vendor.objects.get(name='Encore Chocolate'), orders[4].vendor)

        self.assertEqual(date(2022, 4, 4), orders[start_index].date_ordered)
        self.assertEqual(date(2022, 4, 7), orders[start_index].date_received)
        self.assertEqual(0, orders[start_index].items.count())
        self.assertEqual(Decimal('463'), orders[start_index].net_cost)
        self.assertEqual('Lip Balm and Lip Potion', orders[start_index].notes)
        self.assertIsNone(orders[start_index].payment_method)
        self.assertEqual(0, orders[start_index].receipts.count())
        self.assertEqual('W10004527', orders[start_index].reference_number)
        self.assertEqual(Decimal('24'), orders[start_index].shipping_cost)
        self.assertEqual(Decimal('0'), orders[start_index].tax)
        self.assertEqual(Decimal('487'), orders[start_index].total_cost)
        self.assertEqual(self.user, orders[start_index].user)
        self.assertEqual(Vendor.objects.get(name='Tinte Cosmetics'), orders[start_index].vendor)

        self.assertEqual(date(2022, 7, 21), orders[start_index + 1].date_ordered)
        self.assertIsNone(orders[start_index + 1].date_received)
        self.assertEqual(0, orders[start_index + 1].items.count())
        self.assertEqual(Decimal('14.75'), orders[start_index + 1].net_cost)
        self.assertEqual('essential oils for dry herbs', orders[start_index + 1].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Apple Card'), orders[start_index + 1].payment_method)
        self.assertEqual(0, orders[start_index + 1].receipts.count())
        self.assertEqual('', orders[start_index + 1].reference_number)
        self.assertEqual(Decimal('6.25'), orders[start_index + 1].shipping_cost)
        self.assertEqual(Decimal('0'), orders[start_index + 1].tax)
        self.assertEqual(Decimal('21'), orders[start_index + 1].total_cost)
        self.assertEqual(self.user, orders[start_index + 1].user)
        self.assertEqual(Vendor.objects.get(name='Eden Botanicals'), orders[start_index + 1].vendor)

        self.assertEqual(date(2022, 8, 11), orders[start_index + 2].date_ordered)
        self.assertIsNone(orders[start_index + 2].date_received)
        self.assertEqual(0, orders[start_index + 2].items.count())
        self.assertEqual(Decimal('114'), orders[start_index + 2].net_cost)
        self.assertEqual(
            'Book Page Scultures , Pumpkins and Mushrooms\n\n'
            '* problem – paid through venmo by card we don’t have any idea what it is . Never received bill to pay it',
            orders[start_index + 2].notes
        )
        self.assertEqual(PaymentMethod.objects.get(label='Mastercard 1709'), orders[start_index + 2].payment_method)
        self.assertEqual(0, orders[start_index + 2].receipts.count())
        self.assertEqual('', orders[start_index + 2].reference_number)
        self.assertEqual(Decimal('0'), orders[start_index + 2].shipping_cost)
        self.assertEqual(Decimal('0'), orders[start_index + 2].tax)
        self.assertEqual(Decimal('114'), orders[start_index + 2].total_cost)
        self.assertEqual(self.user, orders[start_index + 2].user)
        self.assertEqual(Vendor.objects.get(name='Root To Vine'), orders[start_index + 2].vendor)

        self.assertEqual(date(2022, 9, 1), orders[start_index + 3].date_ordered)
        self.assertIsNone(orders[start_index + 3].date_received)
        self.assertEqual(0, orders[start_index + 3].items.count())
        self.assertEqual(Decimal('250'), orders[start_index + 3].net_cost)
        self.assertEqual('Hippie Iron On Patch and Journals', orders[start_index + 3].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Apple Card'), orders[start_index + 3].payment_method)
        self.assertEqual(0, orders[start_index + 3].receipts.count())
        self.assertEqual('475656', orders[start_index + 3].reference_number)
        self.assertEqual(Decimal('17.60'), orders[start_index + 3].shipping_cost)
        self.assertEqual(Decimal('0'), orders[start_index + 3].tax)
        self.assertEqual(Decimal('267.60'), orders[start_index + 3].total_cost)
        self.assertEqual(self.user, orders[start_index + 3].user)
        self.assertEqual(Vendor.objects.get(name='Soul Flower'), orders[start_index + 3].vendor)

        self.assertEqual(date(2022, 9, 9), orders[start_index + 4].date_ordered)
        self.assertIsNone(orders[start_index + 4].date_received)
        self.assertEqual(0, orders[start_index + 4].items.count())
        self.assertEqual(Decimal('159.39'), orders[start_index + 4].net_cost)
        self.assertEqual('Pun Mugs', orders[start_index + 4].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Apple Card'), orders[start_index + 4].payment_method)
        self.assertEqual(0, orders[start_index + 4].receipts.count())
        self.assertEqual('10390', orders[start_index + 4].reference_number)
        self.assertEqual(Decimal('59.06'), orders[start_index + 4].shipping_cost)
        self.assertEqual(Decimal('0'), orders[start_index + 4].tax)
        self.assertEqual(Decimal('218.45'), orders[start_index + 4].total_cost)
        self.assertEqual(self.user, orders[start_index + 4].user)
        self.assertEqual(Vendor.objects.get(name='Sarah Edmonds'), orders[start_index + 4].vendor)

        self.assertEqual(date(2022, 9, 9), orders[start_index + 5].date_ordered)
        self.assertEqual(date(2022, 9, 15), orders[start_index + 5].date_received)
        self.assertEqual(0, orders[start_index + 5].items.count())
        self.assertEqual(Decimal('326.10'), orders[start_index + 5].net_cost)
        self.assertEqual('Christmas Ornaments', orders[start_index + 5].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Apple Card'), orders[start_index + 5].payment_method)
        self.assertEqual(0, orders[start_index + 5].receipts.count())
        self.assertEqual('SO4484', orders[start_index + 5].reference_number)
        self.assertEqual(Decimal('0'), orders[start_index + 5].shipping_cost)
        self.assertEqual(Decimal('0'), orders[start_index + 5].tax)
        self.assertEqual(Decimal('326.10'), orders[start_index + 5].total_cost)
        self.assertEqual(self.user, orders[start_index + 5].user)
        self.assertEqual(Vendor.objects.get(name='Cody and Foster'), orders[start_index + 5].vendor)

        self.assertEqual(date(2022, 10, 12), orders[start_index + 6].date_ordered)
        self.assertIsNone(orders[start_index + 6].date_received)
        self.assertEqual(0, orders[start_index + 6].items.count())
        self.assertEqual(Decimal('559'), orders[start_index + 6].net_cost)
        self.assertEqual('Solid Perfumes', orders[start_index + 6].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Apple Card'), orders[start_index + 6].payment_method)
        self.assertEqual(0, orders[start_index + 6].receipts.count())
        self.assertEqual('#4925', orders[start_index + 6].reference_number)
        self.assertEqual(Decimal('0'), orders[start_index + 6].shipping_cost)
        self.assertEqual(Decimal('0'), orders[start_index + 6].tax)
        self.assertEqual(Decimal('559'), orders[start_index + 6].total_cost)
        self.assertEqual(self.user, orders[start_index + 6].user)
        self.assertEqual(Vendor.objects.get(name='Warm Human'), orders[start_index + 6].vendor)

        self.assertEqual(date(2022, 11, 3), orders[start_index + 7].date_ordered)
        self.assertIsNone(orders[start_index + 7].date_received)
        self.assertEqual(0, orders[start_index + 7].items.count())
        self.assertEqual(Decimal('68.73'), orders[start_index + 7].net_cost)
        self.assertEqual('Back Ordered Ornament', orders[start_index + 7].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Apple Card'), orders[start_index + 7].payment_method)
        self.assertEqual(0, orders[start_index + 7].receipts.count())
        self.assertEqual('SO4484', orders[start_index + 7].reference_number)
        self.assertEqual(Decimal('0'), orders[start_index + 7].shipping_cost)
        self.assertEqual(Decimal('0'), orders[start_index + 7].tax)
        self.assertEqual(Decimal('68.73'), orders[start_index + 7].total_cost)
        self.assertEqual(self.user, orders[start_index + 7].user)
        self.assertEqual(Vendor.objects.get(name='Cody and Foster'), orders[start_index + 7].vendor)

        self.assertEqual(date(2022, 11, 6), orders[start_index + 8].date_ordered)
        self.assertEqual(date(2022, 11, 9), orders[start_index + 8].date_received)
        self.assertEqual(0, orders[start_index + 8].items.count())
        self.assertEqual(Decimal('175.50'), orders[start_index + 8].net_cost)
        self.assertEqual('refill of popular items', orders[start_index + 8].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Mastercard 1986'), orders[start_index + 8].payment_method)
        self.assertEqual(0, orders[start_index + 8].receipts.count())
        self.assertEqual('W10005990', orders[start_index + 8].reference_number)
        self.assertEqual(Decimal('9.55'), orders[start_index + 8].shipping_cost)
        self.assertEqual(Decimal('0'), orders[start_index + 8].tax)
        self.assertEqual(Decimal('185.05'), orders[start_index + 8].total_cost)
        self.assertEqual(self.user, orders[start_index + 8].user)
        self.assertEqual(Vendor.objects.get(name='Tinte Cosmetics'), orders[start_index + 8].vendor)

        self.assertEqual(date(2023, 2, 15), orders[start_index + 9].date_ordered)
        self.assertIsNone(orders[start_index + 9].date_received)
        self.assertEqual(0, orders[start_index + 9].items.count())
        self.assertEqual(Decimal('15.45'), orders[start_index + 9].net_cost)
        self.assertEqual('Cranes for resell (intended orig for display)', orders[start_index + 9].notes)
        self.assertIsNone(orders[start_index + 9].payment_method)
        self.assertEqual(0, orders[start_index + 9].receipts.count())
        self.assertEqual('#2798397966 ', orders[start_index + 9].reference_number)
        self.assertEqual(Decimal('6.99'), orders[start_index + 9].shipping_cost)
        self.assertEqual(Decimal('1.80'), orders[start_index + 9].tax)
        self.assertEqual(Decimal('22.44'), orders[start_index + 9].total_cost)
        self.assertEqual(self.user, orders[start_index + 9].user)
        self.assertEqual(Vendor.objects.get(name='PollyNitta – Etsy'), orders[start_index + 9].vendor)

        self.assertEqual(date(2023, 2, 17), orders[start_index + 10].date_ordered)
        self.assertIsNone(orders[start_index + 10].date_received)
        self.assertEqual(0, orders[start_index + 10].items.count())
        self.assertEqual(Decimal('26'), orders[start_index + 10].net_cost)
        self.assertEqual('Cranes for resell (intended orig for display)', orders[start_index + 10].notes)
        self.assertEqual(0, orders[start_index + 10].receipts.count())
        self.assertEqual(0, orders[start_index + 10].receipts.count())
        self.assertEqual('#2796822537 ', orders[start_index + 10].reference_number)
        self.assertEqual(Decimal('6.99'), orders[start_index + 10].shipping_cost)
        self.assertEqual(Decimal('2.64'), orders[start_index + 10].tax)
        self.assertEqual(Decimal('32.99'), orders[start_index + 10].total_cost)
        self.assertEqual(self.user, orders[start_index + 10].user)
        self.assertEqual(Vendor.objects.get(name='PollyNitta – Etsy'), orders[start_index + 10].vendor)

        self.assertEqual(1, mock_success.call_count)
        self.assertEqual(f'Successfully imported {count} orders', mock_success.call_args_list[0][0][1])

    def _check_payment_methods(self):
        payment_methods = PaymentMethod.objects.all()
        self.assertEqual(4, payment_methods.count())

        self.assertEqual('Apple Card', payment_methods[0].label)
        self.assertEqual('Mastercard 1709', payment_methods[1].label)
        self.assertEqual('Mastercard 1986', payment_methods[2].label)
        self.assertEqual('Visa', payment_methods[3].label)

    def _check_vendors(self, missing_vendor_test=False):
        vendors = Vendor.objects.all()
        self.assertEqual(11 if missing_vendor_test else 12, vendors.count())

        self.assertEqual('Cody and Foster', vendors[0].name)
        self.assertEqual(Decimal('2825.88'), vendors[0].running_investment)
        self.assertEqual('', vendors[0].website)

        self.assertEqual('Dzi Handmade', vendors[1].name)
        self.assertEqual(Decimal('152.29'), vendors[1].running_investment)
        self.assertEqual('', vendors[1].website)

        self.assertEqual('Eden Botanicals', vendors[2].name)
        self.assertEqual(Decimal('1086.95'), vendors[2].running_investment)
        self.assertEqual('', vendors[2].website)
        
        if missing_vendor_test:
            start_index = 3
        else:
            start_index = 4

            self.assertEqual('Encore Chocolate', vendors[3].name)
            self.assertEqual(Decimal('323.95'), vendors[3].running_investment)
            self.assertEqual('', vendors[3].website)

        self.assertEqual('Insanely Paracord', vendors[start_index].name)
        self.assertEqual(Decimal('1065.95'), vendors[start_index].running_investment)
        self.assertEqual('https://insanelyparacord.com', vendors[start_index].website)

        self.assertEqual('PollyNitta – Etsy', vendors[start_index + 1].name)
        self.assertEqual(Decimal('2881.31'), vendors[start_index + 1].running_investment)
        self.assertEqual('', vendors[start_index + 1].website)

        self.assertEqual('Root To Vine', vendors[start_index + 2].name)
        self.assertEqual(Decimal('1200.95'), vendors[start_index + 2].running_investment)
        self.assertEqual('Etsy', vendors[start_index + 2].website)

        self.assertEqual('Sarah Edmonds', vendors[start_index + 3].name)
        self.assertEqual(Decimal('1419.40'), vendors[start_index + 3].running_investment)
        self.assertEqual('https://www.sarahedmondsillustration.com/tradeorders', vendors[start_index + 3].website)

        self.assertEqual('Soul Flower', vendors[start_index + 4].name)
        self.assertEqual(Decimal('1687'), vendors[start_index + 4].running_investment)
        self.assertEqual('https://www.soul-flower.com/mm5/merchant.mvc?Screen=ACLN', vendors[start_index + 4].website)

        self.assertEqual('Starwest Botanicals', vendors[start_index + 5].name)
        self.assertEqual(Decimal('233.95'), vendors[start_index + 5].running_investment)
        self.assertEqual('https://wholesale.starwest-botanicals.com/', vendors[start_index + 5].website)

        self.assertEqual('Tinte Cosmetics', vendors[start_index + 6].name)
        self.assertEqual(Decimal('2757.15'), vendors[start_index + 6].running_investment)
        self.assertEqual('', vendors[start_index + 6].website)

        self.assertEqual('Warm Human', vendors[start_index + 7].name)
        self.assertEqual(Decimal('2572.10'), vendors[start_index + 7].running_investment)
        self.assertEqual('', vendors[start_index + 7].website)
