def Navigation(on):
    navigation = (
        ["Add Item",        "/shopowner/inventory/add/"],       # index 0
        ["Edit Item",       "/shopowner/inventory/edit/"],      # index 1
        ["List Items",      "/shopowner/inventory/list/"],      # index 2
        ["",                ""],                                # index 3
        ["Add Seller",      "/shopowner/seller/add/"],          # index 4
        ["Edit Seller",     "/shopowner/seller/edit/"],         # index 5
        ["List Sellers",    "/shopowner/seller/list/"],         # index 6
    )

    if on == "add_item":
        navigation[0][1] = ""
    elif on == "edit_item":
        navigation[1][1] = ""
    elif on == "list_items":
        navigation[2][1] = ""
    elif on == "add_seller":
        navigation[4][1] = ""
    elif on == "edit_seller":
        navigation[5][1] = ""
    elif on == "list_sellers":
        navigation[6][1] = ""

    return navigation

