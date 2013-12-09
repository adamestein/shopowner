def Navigation(on):
    navigation = (
        ["Add Item",        "/shopowner/inventory/add/"],       # index 0
        ["Edit Item",       "/shopowner/inventory/edit/"],      # index 1
        ["List Items",      "/shopowner/inventory/list/"],      # index 2
        ["",                ""],                                # index 3
        ["Add Category",    "/shopowner/category/add/"],        # index 4
        ["Edit Category",   "/shopowner/category/edit/"],       # index 5
        ["List Categories", "/shopowner/category/list/"],       # index 6
        ["",                ""],                                # index 7
        ["Add Seller",      "/shopowner/seller/add/"],          # index 8
        ["Edit Seller",     "/shopowner/seller/edit/"],         # index 9
        ["List Sellers",    "/shopowner/seller/list/"],         # index 10
    )

    if on == "add_item":
        navigation[0][1] = ""
    elif on == "edit_item":
        navigation[1][1] = ""
    elif on == "list_items":
        navigation[2][1] = ""
    elif on == "add_category":
        navigation[4][1] = ""
    elif on == "edit_category":
        navigation[5][1] = ""
    elif on == "list_categories":
        navigation[6][1] = ""
    elif on == "add_seller":
        navigation[8][1] = ""
    elif on == "edit_seller":
        navigation[9][1] = ""
    elif on == "list_sellers":
        navigation[10][1] = ""

    return navigation

