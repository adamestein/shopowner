from csv import DictReader
from decimal import Decimal
import io

from pyexcel_odsr import get_data

from django.contrib.messages import success
from django.urls import reverse_lazy

from .forms import ImportForm

from inventory.models import Inventory, Vendor

from library.formats import MIMETYPE_CSV, convert_currency_text
from library.lists import get_list_value
from library.views.generic import AppFormView

HEADER = [
    'Stock Number',
    'Item',
    'Supplier',
    'There Product #',
    'Wholesale Price/Unit Price',
    'Qty Purchased',
    'Priced',
    'Sold',
    'Gifted or Other',
    'Remaining',
    ''
]


class ImportView(AppFormView):
    form_class = ImportForm
    success_url = reverse_lazy('data_transfer:import')
    template_name = 'data_transfer/import.html'

    def form_valid(self, form):
        try:
            if form.filetype == MIMETYPE_CSV:
                read_func = self._read_csv
            else:
                read_func = self._read_ods

            num_items = read_func(self.request.user, form['file'].data)

            success(self.request, f'Successfully imported {num_items} items into your inventory')

            return super().form_valid(form)
        except RuntimeError as e:
            form.add_error('file', e)
            return self.form_invalid(form)

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def _read_csv(self, user, data):
        reader = DictReader(io.TextIOWrapper(data, encoding='utf-8-sig', errors='replace'))

        if reader.fieldnames == HEADER:
            num_items = 0

            for row in reader:
                self._save_data(user, row)
                num_items += 1

            return num_items
        else:
            raise RuntimeError(f'Header mismatch for "{data.name}"')

    def _read_ods(self, user, data):
        tabs = get_data(data)

        try:
            # Don't get the empty header string on the last column with data like for CSV, so remove for header test
            if tabs['Inventory'][0] == HEADER[:-1]:
                num_items = 0

                for row in tabs['Inventory'][1:]:
                    if len(row):
                        self._save_data(
                            user,
                            {
                                '': get_list_value(row, 10),
                                'Gifted or Other': get_list_value(row, 8),
                                'Item': row[1],
                                'Priced': get_list_value(row, 6),
                                'Qty Purchased': get_list_value(row, 5, default_value=0),
                                'Sold': get_list_value(row, 7),
                                'Stock Number': row[0],
                                'Supplier': get_list_value(row, 2, default_value=None),
                                'There Product #': get_list_value(row, 3),
                                'Wholesale Price/Unit Price': get_list_value(row, 4)
                            }
                        )

                        num_items += 1

                return num_items
            else:
                raise RuntimeError(f'Header mismatch for "{data.name}" on the Inventory tab')
        except KeyError:
            raise RuntimeError(f'Inventory tab not found in "{data.name}"')

    @staticmethod
    def _save_data(user, row):
        vendor, _ = Vendor.objects.get_or_create(name=row['Supplier']) if row['Supplier'] else (None, None)

        if row['Wholesale Price/Unit Price'] == '':
            if row['Qty Purchased']:
                # We can calculate the missing wholesale price using the purchase price divided by the
                # number of items purchased
                if row['Priced']:
                    total_price = Decimal(convert_currency_text(row['Priced']))
                elif row['']:
                    total_price = Decimal(convert_currency_text(row['']))
                else:
                    # Don't have the purchase price
                    total_price = Decimal('0.00')

                price = total_price / Decimal(row['Qty Purchased'])
            else:
                # Don't have a wholesale price and don't have enough data to figure it out
                price = Decimal('0.00')
        else:
            price = Decimal(convert_currency_text(row['Wholesale Price/Unit Price']))

        sold = int(row['Sold']) if row['Sold'] else 0

        record, created = Inventory.objects.get_or_create(
            label=row['Item'],
            product_number=row['There Product #'],
            stock_number=row['Stock Number'],
            vendor=vendor,
            user=user,
            defaults={
                'notes': row['Gifted or Other'].strip(),
                'qty_bought': int(row['Qty Purchased']),
                'qty_sold': sold,
                'wholesale_price': price
            }
        )

        if not created:
            # Updating with new information
            if row['Gifted or Other'].strip():
                record.notes += '\n' + row['Gifted or Other'].strip()
            record.qty_bought = int(row['Qty Purchased'])
            record.qty_sold = sold
            record.wholesale_price = price
            record.save()
