def Navigation(on):
    navigation = (
        ["Inventory", "/shopowner/inventory/"],   # index 0
        ["Sales", "/shopowner/sales/"],           # index 1
    )

    if on == "inventory":
        navigation[0][1] = ""
    elif on == "sales":
        navigation[1][1] = ""

    return navigation

