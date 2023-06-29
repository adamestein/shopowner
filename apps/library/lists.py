def get_list_value(values, index, default_value=''):
    try:
        return values[index]
    except IndexError:
        return default_value
