def Navigation(on):
    navigation = (
        ["Record Sale",         "/shopowner/sales/record/"],            # index 0
        ["View Sales",          "/shopowner/sales/view/"],              # index 1
        ["",                    ""],                                    # index 2
        ["Update Sales Tax",    "/shopowner/sales/update/tax/"],        # index 3
    )

    if on == "record_sale":
        navigation[0][1] = ""
    elif on == "view_sales":
        navigation[1][1] = ""
    elif on == "update_sales_tax":
        navigation[3][1] = ""

    return navigation

