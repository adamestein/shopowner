from datetime import date
from decimal import Decimal
from os.path import join
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from ..import_data.orders import ImportView

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
            'Orders tab not found in "missing_tabs.ods"',
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
            'Header mismatch for "bad_order_header.ods" on the Orders tab',
            response.context_data['form'].errors['file'].data[0].message.args[0]
        )

        self.assertEqual(0, mock_success.call_count)

    def test_missing_vendor_csv(self, mock_success):
        with open(join(self.data_dir, 'missing_vendor.csv'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        self.assertEqual(
            'Missing vendor in "missing_vendor.csv" (line 4)',
            response.context_data['form'].errors['file'].data[0].message.args[0]
        )

        self.assertEqual(0, mock_success.call_count)

    def test_missing_vendor_ods(self, mock_success):
        with open(join(self.data_dir, 'missing_vendor.ods'), 'rb') as input_file:
            request = RequestFactory().post('/', {'file': input_file})
            request.user = self.user

        view = setup_view(ImportView(), request)

        response = view.post(request)

        self.assertEqual(
            'Missing vendor in "missing_vendor.ods" (line 4)',
            response.context_data['form'].errors['file'].data[0].message.args[0]
        )

        self.assertEqual(0, mock_success.call_count)

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

    def _check_data(self, mock_success):
        orders = Order.objects.all()
        self.assertEqual(16, orders.count())

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

        self.assertEqual(date(2022, 4, 4), orders[5].date_ordered)
        self.assertEqual(date(2022, 4, 7), orders[5].date_received)
        self.assertEqual(0, orders[5].items.count())
        self.assertEqual(Decimal('463'), orders[5].net_cost)
        self.assertEqual('Lip Balm and Lip Potion', orders[5].notes)
        self.assertIsNone(orders[5].payment_method)
        self.assertEqual(0, orders[5].receipts.count())
        self.assertEqual('W10004527', orders[5].reference_number)
        self.assertEqual(Decimal('24'), orders[5].shipping_cost)
        self.assertEqual(Decimal('0'), orders[5].tax)
        self.assertEqual(Decimal('487'), orders[5].total_cost)
        self.assertEqual(self.user, orders[5].user)
        self.assertEqual(Vendor.objects.get(name='Tinte Cosmetics'), orders[5].vendor)

        self.assertEqual(date(2022, 7, 21), orders[6].date_ordered)
        self.assertIsNone(orders[6].date_received)
        self.assertEqual(0, orders[6].items.count())
        self.assertEqual(Decimal('14.75'), orders[6].net_cost)
        self.assertEqual('essential oils for dry herbs', orders[6].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Apple Card'), orders[6].payment_method)
        self.assertEqual(0, orders[6].receipts.count())
        self.assertEqual('', orders[6].reference_number)
        self.assertEqual(Decimal('6.25'), orders[6].shipping_cost)
        self.assertEqual(Decimal('0'), orders[6].tax)
        self.assertEqual(Decimal('21'), orders[6].total_cost)
        self.assertEqual(self.user, orders[6].user)
        self.assertEqual(Vendor.objects.get(name='Eden Botanicals'), orders[6].vendor)

        self.assertEqual(date(2022, 8, 11), orders[7].date_ordered)
        self.assertIsNone(orders[7].date_received)
        self.assertEqual(0, orders[7].items.count())
        self.assertEqual(Decimal('114'), orders[7].net_cost)
        self.assertEqual(
            'Book Page Scultures , Pumpkins and Mushrooms\n\n'
            '* problem – paid through venmo by card we don’t have any idea what it is . Never received bill to pay it',
            orders[7].notes
        )
        self.assertEqual(PaymentMethod.objects.get(label='Mastercard 1709'), orders[7].payment_method)
        self.assertEqual(0, orders[7].receipts.count())
        self.assertEqual('', orders[7].reference_number)
        self.assertEqual(Decimal('0'), orders[7].shipping_cost)
        self.assertEqual(Decimal('0'), orders[7].tax)
        self.assertEqual(Decimal('114'), orders[7].total_cost)
        self.assertEqual(self.user, orders[7].user)
        self.assertEqual(Vendor.objects.get(name='Root To Vine'), orders[7].vendor)

        self.assertEqual(date(2022, 9, 1), orders[8].date_ordered)
        self.assertIsNone(orders[8].date_received)
        self.assertEqual(0, orders[8].items.count())
        self.assertEqual(Decimal('250'), orders[8].net_cost)
        self.assertEqual('Hippie Iron On Patch and Journals', orders[8].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Apple Card'), orders[8].payment_method)
        self.assertEqual(0, orders[8].receipts.count())
        self.assertEqual('475656', orders[8].reference_number)
        self.assertEqual(Decimal('17.60'), orders[8].shipping_cost)
        self.assertEqual(Decimal('0'), orders[8].tax)
        self.assertEqual(Decimal('267.60'), orders[8].total_cost)
        self.assertEqual(self.user, orders[8].user)
        self.assertEqual(Vendor.objects.get(name='Soul Flower'), orders[8].vendor)

        self.assertEqual(date(2022, 9, 9), orders[9].date_ordered)
        self.assertIsNone(orders[9].date_received)
        self.assertEqual(0, orders[9].items.count())
        self.assertEqual(Decimal('159.39'), orders[9].net_cost)
        self.assertEqual('Pun Mugs', orders[9].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Apple Card'), orders[9].payment_method)
        self.assertEqual(0, orders[9].receipts.count())
        self.assertEqual('10390', orders[9].reference_number)
        self.assertEqual(Decimal('59.06'), orders[9].shipping_cost)
        self.assertEqual(Decimal('0'), orders[9].tax)
        self.assertEqual(Decimal('218.45'), orders[9].total_cost)
        self.assertEqual(self.user, orders[9].user)
        self.assertEqual(Vendor.objects.get(name='Sarah Edmonds'), orders[9].vendor)

        self.assertEqual(date(2022, 9, 9), orders[10].date_ordered)
        self.assertEqual(date(2022, 9, 15), orders[10].date_received)
        self.assertEqual(0, orders[10].items.count())
        self.assertEqual(Decimal('326.10'), orders[10].net_cost)
        self.assertEqual('Christmas Ornaments', orders[10].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Apple Card'), orders[10].payment_method)
        self.assertEqual(0, orders[10].receipts.count())
        self.assertEqual('SO4484', orders[10].reference_number)
        self.assertEqual(Decimal('0'), orders[10].shipping_cost)
        self.assertEqual(Decimal('0'), orders[10].tax)
        self.assertEqual(Decimal('326.10'), orders[10].total_cost)
        self.assertEqual(self.user, orders[10].user)
        self.assertEqual(Vendor.objects.get(name='Cody and Foster'), orders[10].vendor)

        self.assertEqual(date(2022, 10, 12), orders[11].date_ordered)
        self.assertIsNone(orders[11].date_received)
        self.assertEqual(0, orders[11].items.count())
        self.assertEqual(Decimal('559'), orders[11].net_cost)
        self.assertEqual('Solid Perfumes', orders[11].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Apple Card'), orders[11].payment_method)
        self.assertEqual(0, orders[11].receipts.count())
        self.assertEqual('#4925', orders[11].reference_number)
        self.assertEqual(Decimal('0'), orders[11].shipping_cost)
        self.assertEqual(Decimal('0'), orders[11].tax)
        self.assertEqual(Decimal('559'), orders[11].total_cost)
        self.assertEqual(self.user, orders[11].user)
        self.assertEqual(Vendor.objects.get(name='Warm Human'), orders[11].vendor)

        self.assertEqual(date(2022, 11, 3), orders[12].date_ordered)
        self.assertIsNone(orders[12].date_received)
        self.assertEqual(0, orders[12].items.count())
        self.assertEqual(Decimal('68.73'), orders[12].net_cost)
        self.assertEqual('Back Ordered Ornament', orders[12].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Apple Card'), orders[12].payment_method)
        self.assertEqual(0, orders[12].receipts.count())
        self.assertEqual('SO4484', orders[12].reference_number)
        self.assertEqual(Decimal('0'), orders[12].shipping_cost)
        self.assertEqual(Decimal('0'), orders[12].tax)
        self.assertEqual(Decimal('68.73'), orders[12].total_cost)
        self.assertEqual(self.user, orders[12].user)
        self.assertEqual(Vendor.objects.get(name='Cody and Foster'), orders[12].vendor)

        self.assertEqual(date(2022, 11, 6), orders[13].date_ordered)
        self.assertEqual(date(2022, 11, 9), orders[13].date_received)
        self.assertEqual(0, orders[13].items.count())
        self.assertEqual(Decimal('175.50'), orders[13].net_cost)
        self.assertEqual('refill of popular items', orders[13].notes)
        self.assertEqual(PaymentMethod.objects.get(label='Mastercard 1986'), orders[13].payment_method)
        self.assertEqual(0, orders[13].receipts.count())
        self.assertEqual('W10005990', orders[13].reference_number)
        self.assertEqual(Decimal('9.55'), orders[13].shipping_cost)
        self.assertEqual(Decimal('0'), orders[13].tax)
        self.assertEqual(Decimal('185.05'), orders[13].total_cost)
        self.assertEqual(self.user, orders[13].user)
        self.assertEqual(Vendor.objects.get(name='Tinte Cosmetics'), orders[13].vendor)

        self.assertEqual(date(2023, 2, 15), orders[14].date_ordered)
        self.assertIsNone(orders[14].date_received)
        self.assertEqual(0, orders[14].items.count())
        self.assertEqual(Decimal('15.45'), orders[14].net_cost)
        self.assertEqual('Cranes for resell (intended orig for display)', orders[14].notes)
        self.assertIsNone(orders[14].payment_method)
        self.assertEqual(0, orders[14].receipts.count())
        self.assertEqual('#2798397966 ', orders[14].reference_number)
        self.assertEqual(Decimal('6.99'), orders[14].shipping_cost)
        self.assertEqual(Decimal('1.80'), orders[14].tax)
        self.assertEqual(Decimal('22.44'), orders[14].total_cost)
        self.assertEqual(self.user, orders[14].user)
        self.assertEqual(Vendor.objects.get(name='PollyNitta – Etsy'), orders[14].vendor)

        self.assertEqual(date(2023, 2, 17), orders[15].date_ordered)
        self.assertIsNone(orders[15].date_received)
        self.assertEqual(0, orders[15].items.count())
        self.assertEqual(Decimal('26'), orders[15].net_cost)
        self.assertEqual('Cranes for resell (intended orig for display)', orders[15].notes)
        self.assertEqual(0, orders[15].receipts.count())
        self.assertEqual(0, orders[15].receipts.count())
        self.assertEqual('#2796822537 ', orders[15].reference_number)
        self.assertEqual(Decimal('6.99'), orders[15].shipping_cost)
        self.assertEqual(Decimal('2.64'), orders[15].tax)
        self.assertEqual(Decimal('32.99'), orders[15].total_cost)
        self.assertEqual(self.user, orders[15].user)
        self.assertEqual(Vendor.objects.get(name='PollyNitta – Etsy'), orders[15].vendor)

        self.assertEqual(1, mock_success.call_count)
        self.assertEqual('Successfully imported 16 orders', mock_success.call_args_list[0][0][1])

    def _check_payment_methods(self):
        payment_methods = PaymentMethod.objects.all()
        self.assertEqual(4, payment_methods.count())

        self.assertEqual('Apple Card', payment_methods[0].label)
        self.assertEqual('Mastercard 1709', payment_methods[1].label)
        self.assertEqual('Mastercard 1986', payment_methods[2].label)
        self.assertEqual('Visa', payment_methods[3].label)

    def _check_vendors(self):
        vendors = Vendor.objects.all()
        self.assertEqual(12, vendors.count())

        self.assertEqual('Cody and Foster', vendors[0].name)
        self.assertEqual(Decimal('2825.88'), vendors[0].running_investment)
        self.assertEqual('', vendors[0].website)

        self.assertEqual('Dzi Handmade', vendors[1].name)
        self.assertEqual(Decimal('152.29'), vendors[1].running_investment)
        self.assertEqual('', vendors[1].website)

        self.assertEqual('Eden Botanicals', vendors[2].name)
        self.assertEqual(Decimal('1086.95'), vendors[2].running_investment)
        self.assertEqual('', vendors[2].website)

        self.assertEqual('Encore Chocolate', vendors[3].name)
        self.assertEqual(Decimal('323.95'), vendors[3].running_investment)
        self.assertEqual('', vendors[3].website)

        self.assertEqual('Insanely Paracord', vendors[4].name)
        self.assertEqual(Decimal('1065.95'), vendors[4].running_investment)
        self.assertEqual('https://insanelyparacord.com', vendors[4].website)

        self.assertEqual('PollyNitta – Etsy', vendors[5].name)
        self.assertEqual(Decimal('2881.31'), vendors[5].running_investment)
        self.assertEqual('', vendors[5].website)

        self.assertEqual('Root To Vine', vendors[6].name)
        self.assertEqual(Decimal('1200.95'), vendors[6].running_investment)
        self.assertEqual('Etsy', vendors[6].website)

        self.assertEqual('Sarah Edmonds', vendors[7].name)
        self.assertEqual(Decimal('1419.40'), vendors[7].running_investment)
        self.assertEqual('https://www.sarahedmondsillustration.com/tradeorders', vendors[7].website)

        self.assertEqual('Soul Flower', vendors[8].name)
        self.assertEqual(Decimal('1687'), vendors[8].running_investment)
        self.assertEqual('https://www.soul-flower.com/mm5/merchant.mvc?Screen=ACLN', vendors[8].website)

        self.assertEqual('Starwest Botanicals', vendors[9].name)
        self.assertEqual(Decimal('233.95'), vendors[9].running_investment)
        self.assertEqual('https://wholesale.starwest-botanicals.com/', vendors[9].website)

        self.assertEqual('Tinte Cosmetics', vendors[10].name)
        self.assertEqual(Decimal('2757.15'), vendors[10].running_investment)
        self.assertEqual('', vendors[10].website)

        self.assertEqual('Warm Human', vendors[11].name)
        self.assertEqual(Decimal('2572.10'), vendors[11].running_investment)
        self.assertEqual('', vendors[11].website)
