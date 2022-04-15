from django.urls import reverse_lazy


def navigation(on):
    narray = (
        ["Record Sale", reverse_lazy('sales:record')],      # index 0
        ["Edit Sale", reverse_lazy('sales:edit')],          # index 1
        ["", ""],                                           # index 2
        ["View Sales", reverse_lazy('sales:view')],         # index 3
    )

    if on == "record_sale":
        narray[0][1] = ""
    elif on == "edit_sale":
        narray[1][1] = ""
    elif on == "view_sales":
        narray[3][1] = ""

    return narray

