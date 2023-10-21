# Mimetype file formats
MIMETYPE_CSV = 'application/csv'
MIMETYPE_ODS = 'application/vnd.oasis.opendocument.spreadsheet'
MIMETYPE_PLAIN = 'text/plain'   # CSV files could look like plain text files


def convert_currency_text(text, label, line_num):
    # Convert any currency text that contains $ signs or USD units a float that is rounded at 2 decimal points
    try:
        return round(float(text.replace('$', '').replace(',', '').replace(' USD', '')), 2)
    except ValueError:
        raise RuntimeError(f'{label} not a numeric value, found "{text}" instead (line {line_num})')
