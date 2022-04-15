def calculate_sale_price(price, discount, tax_rate):
    discount_amt = price * (discount / 100.0)
    price -= discount_amt
    tax_amt = price * (tax_rate / 100.0)

    # Make sure we round up (other rounding methods didn't work in all cases
    # for currency)
    return round_currency(price + tax_amt)


def round_currency(value):
    # Round for currency's 2 digits
    return float(int((value + 0.005) * 100.0) / 100.0)

