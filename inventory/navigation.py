def navigation(on):
    narray = (
        ["Add Item", "/shopowner/inventory/add/"],       # index 0
        ["Edit Item", "/shopowner/inventory/edit/"],      # index 1
        ["List Items", "/shopowner/inventory/list/"],      # index 2
        ["", ""],                                # index 3
        ["Add Category", "/shopowner/category/add/"],        # index 4
        ["Edit Category", "/shopowner/category/edit/"],       # index 5
        ["List Categories", "/shopowner/category/list/"],       # index 6
        ["", ""],                                # index 7
        ["Add Seller", "/shopowner/seller/add/"],          # index 8
        ["Edit Seller", "/shopowner/seller/edit/"],         # index 9
        ["List Sellers", "/shopowner/seller/list/"],         # index 10
    )

    if on == "add_item":
        narray[0][1] = ""
    elif on == "edit_item":
        narray[1][1] = ""
    elif on == "list_items":
        narray[2][1] = ""
    elif on == "add_category":
        narray[4][1] = ""
    elif on == "edit_category":
        narray[5][1] = ""
    elif on == "list_categories":
        narray[6][1] = ""
    elif on == "add_seller":
        narray[8][1] = ""
    elif on == "edit_seller":
        narray[9][1] = ""
    elif on == "list_sellers":
        narray[10][1] = ""

    return narray

