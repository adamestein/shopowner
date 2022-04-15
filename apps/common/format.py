# Format currency depending on Python version (v2.7 and greater is one way,
# v2.6 and less is another way)
def currency(amount):
    import sys

    major_minor = sys.version_info[0]*10+sys.version_info[1]

    if major_minor >= 27:
        return "${:0,.2f}".format(amount)
    else:
        import locale

        return locale.currency(amount, grouping=True)

# Format number with commas depending on Python version (v2.7 and greater is
# one way, v2.6 and less is another way)
def with_commas(amount, prec=6):
    import sys

    major_minor = sys.version_info[0]*10+sys.version_info[1]

    if major_minor >= 27:
        fmt = "{:0,.%df}" % prec

        return fmt.format(amount)
    else:
        import locale

        fmt = "%.%df" % prec

        return locale.format(fmt, amount, grouping=True)

