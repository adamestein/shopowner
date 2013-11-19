from decimal import *

def calculate_sale_price(price, discount, tax_rate):
    discount_amt = price*(discount/100.0)
    price = price - discount_amt
    tax_amt = price*(tax_rate/100.0)

    # Make sure we round up (other rounding methods didn't work in all cases
    # for currency)
    return float(int((price+tax_amt+0.005)*100.0)/100.0)

