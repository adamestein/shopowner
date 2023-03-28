# Mimetype file formats
MIMETYPE_CSV = 'application/csv'
MIMETYPE_ODS = 'application/vnd.oasis.opendocument.spreadsheet'


def convert_currency_text(text):
    # Convert any currency text that contains $ signs or USD units a float that is rounded at 2 decimal points
    return round(float(text.replace('$', '').replace(' USD', '')), 2)
