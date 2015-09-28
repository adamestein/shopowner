def navigation(on):
    narray = (
        ["Add Item", "/shopowner/inventory/add/"],              # index 0
        ["Edit Item", "/shopowner/inventory/edit/"],            # index 1
        ["List Items", "/shopowner/inventory/list/"],           # index 2
        ["Image Sheet", "/shopowner/inventory/image_sheet"],    # index 3
        ["", ""],                                               # index 4
        ["Add Category", "/shopowner/category/add/"],           # index 5
        ["Edit Category", "/shopowner/category/edit/"],         # index 6
        ["List Categories", "/shopowner/category/list/"],       # index 7
        ["", ""],                                               # index 8
        ["Add Seller", "/shopowner/seller/add/"],               # index 9
        ["Edit Seller", "/shopowner/seller/edit/"],             # index 10
        ["List Sellers", "/shopowner/seller/list/"],            # index 11
    )

    if on == "add_item":
        narray[0][1] = ""
    elif on == "edit_item":
        narray[1][1] = ""
    elif on == "list_items":
        narray[2][1] = ""
    elif on == "image_sheet":
        narray[3][1] = ""
    elif on == "add_category":
        narray[5][1] = ""
    elif on == "edit_category":
        narray[6][1] = ""
    elif on == "list_categories":
        narray[7][1] = ""
    elif on == "add_seller":
        narray[9][1] = ""
    elif on == "edit_seller":
        narray[10][1] = ""
    elif on == "list_sellers":
        narray[11][1] = ""

    return narray

