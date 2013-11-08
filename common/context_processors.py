from django.conf import settings

def version(request):
    if settings.DEBUG == True:
        mode = "(Development) "
    else:
        mode = ""

    version_dict = {
        "version": "Shop Owner Apps %sv" % mode + settings.VERSION
    }

    return version_dict

