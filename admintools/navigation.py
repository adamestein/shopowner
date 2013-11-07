def ATNavigation(on):
    navigation = (
        ["Database Copy",   "/admin/tools/dbcopy/"],   # index 0
        ["", ""],
        ["Django Admin",    "/admin/"],                # index 2
    )

    if on == "dbcopy":
        navigation[0][1] = ""

    return navigation

