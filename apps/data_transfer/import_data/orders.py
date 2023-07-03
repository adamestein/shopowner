from csv import DictReader
from datetime import datetime
import io

from pyexcel_odsr import get_data

from django.contrib.messages import success
from django.db import transaction
from django.urls import reverse_lazy

from data_transfer.import_data.forms import ImportForm

from library.formats import MIMETYPE_CSV, MIMETYPE_PLAIN, convert_currency_text
from library.lists import get_list_value
from library.views.generic import AppFormView

from orders.models import Order, PaymentMethod

from vendors.models import Vendor

HEADER = [
    '',
    'Date Ordered',
    'Date Received',
    'Order #/Ref',
    'Company',
    'Company Email Site',
    'Items',
    'Net Cost',
    'Tax Credit Paid',
    'Shipping Cost',
    'Total Cost',
    'Running Investment',
    'Payment Used',
    'Receipt',
    'Notes'
]


class ImportView(AppFormView):
    form_class = ImportForm
    success_url = reverse_lazy('data_transfer:import_orders')
    template_name = 'data_transfer/import/orders.html'

    def form_valid(self, form):
        try:
            if form.filetype in [MIMETYPE_CSV, MIMETYPE_PLAIN]:
                read_func = self._read_csv
            else:
                read_func = self._read_ods

            with transaction.atomic():
                num_items = read_func(self.request.user, form['file'].data)

            success(self.request, f'Successfully imported {num_items} orders')

            return super().form_valid(form)
        except RuntimeError as e:
            form.add_error('file', e)
            return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @staticmethod
    def _create_notes(items, notes):
        if items and notes:
            return items + '\n\n' + notes
        elif not notes:
            return items
        else:
            return notes

    def _read_csv(self, user, data):
        reader = DictReader(io.TextIOWrapper(data, encoding='utf-8-sig', errors='replace'))

        if reader.fieldnames == HEADER:
            num_items = 0

            for row in reader:
                if row['Date Ordered']:
                    row['Date Ordered'] = datetime.strptime(row['Date Ordered'], '%m/%d/%y').date()

                if row['Date Received']:
                    row['Date Received'] = datetime.strptime(row['Date Received'], '%m/%d/%y').date()

                row['Notes'] = self._create_notes(row['Items'], row['Notes'])

                self._save_data(data, reader.line_num, user, row)
                num_items += 1

            return num_items
        else:
            raise RuntimeError(f'Header mismatch for "{data.name}"')

    def _read_ods(self, user, data):
        tabs = get_data(data)

        try:
            # Don't get the empty header string on the last column with data like for CSV, so remove for header test
            if tabs['Orders'][0] == HEADER:
                num_items = 0

                for line_num, row in enumerate(tabs['Orders'][1:], start=2):
                    if len(row):
                        self._save_data(
                            data,
                            line_num,
                            user,
                            {
                                'Company': get_list_value(row, 4),
                                'Company Email Site': get_list_value(row, 5),
                                'Date Ordered': get_list_value(row, 1, default_value=None),
                                'Date Received': get_list_value(row, 2, default_value=None),
                                'Net Cost': row[7],
                                'Notes': self._create_notes(get_list_value(row, 6), get_list_value(row, 14)),
                                'Payment Used': get_list_value(row, 12, default_value=None),
                                'Order #/Ref': get_list_value(row, 3),
                                'Running Investment': row[11],
                                'Shipping Cost': get_list_value(row, 9),
                                'Tax Credit Paid': get_list_value(row, 8)
                            }
                        )

                        num_items += 1

                return num_items
            else:
                raise RuntimeError(f'Header mismatch for "{data.name}" on the Order tab')
        except KeyError:
            raise RuntimeError(f'Orders tab not found in "{data.name}"')

    @staticmethod
    def _save_data(data, line_num, user, row):
        if not row['Company']:
            raise RuntimeError(f'Missing vendor in "{data.name}" (line {line_num})')

        if row['Date Ordered'] and row['Date Received'] and row['Date Received'] < row['Date Ordered']:
            raise RuntimeError(f'Received date is BEFORE the order date in "{data.name}" (line {line_num})')

        if not row['Net Cost']:
            raise RuntimeError(f'Missing net cost in "{data.name}" (line {line_num})')

        if row['Payment Used']:
            payment_method, _ = PaymentMethod.objects.get_or_create(label=row['Payment Used'])
        else:
            payment_method = None

        vendor, _ = Vendor.objects.get_or_create(name=row['Company'])

        vendor.running_investment = convert_currency_text(row['Running Investment'])
        vendor.website = row['Company Email Site']
        vendor.save()

        Order.objects.create(
            date_ordered=row['Date Ordered'] or None,
            date_received=row['Date Received'] or None,
            net_cost=convert_currency_text(row['Net Cost']),
            notes=row['Notes'],
            payment_method=payment_method,
            reference_number=str(row['Order #/Ref']).encode('ascii', 'ignore'),
            shipping_cost=convert_currency_text(row['Shipping Cost'] or '0'),
            tax=convert_currency_text(row['Tax Credit Paid'] or '0'),
            vendor=vendor,
            user=user
        )
