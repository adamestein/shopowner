from django.urls import reverse_lazy


def navigation(on):
    narray = (
        ["Add Item", reverse_lazy('item:add')],                 # index 0
        ["Edit Item", reverse_lazy('item:edit')],               # index 1
        ["List Items", reverse_lazy('item:list')],              # index 2
        ["Image Sheet", reverse_lazy('item:image_sheet')],      # index 3
        ["", ""],                                               # index 4
        ["Add Category", reverse_lazy('category:add')],         # index 5
        ["Edit Category", reverse_lazy('category:edit')],       # index 6
        ["List Categories", reverse_lazy('category:list')],     # index 7
        ["", ""],                                               # index 8
        ["Add Seller", reverse_lazy('seller:add')],             # index 9
        ["Edit Seller", reverse_lazy('seller:edit')],           # index 10
        ["List Sellers", reverse_lazy('seller:list')],          # index 11
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

