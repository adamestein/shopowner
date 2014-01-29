def Navigation(on):
    navigation = (
        ["Record Sale", "/shopowner/sales/record/"],    # index 0
        ["Edit Sale", "/shopowner/sales/edit/"],        # index 1
        ["", ""],                                       # index 2
        ["View Sales", "/shopowner/sales/view/"],       # index 3
    )

    if on == "record_sale":
        navigation[0][1] = ""
    elif on == "edit_sale":
        navigation[1][1] = ""
    elif on == "view_sales":
        navigation[3][1] = ""

    return navigation

