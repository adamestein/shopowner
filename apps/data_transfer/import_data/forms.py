# noinspection PyPackageRequirements
import magic

from django import forms

from library.formats import MIMETYPE_CSV, MIMETYPE_ODS, MIMETYPE_PLAIN


class ImportForm(forms.Form):
    file = forms.FileField()
    filetype = None

    def clean_file(self):
        data = self.cleaned_data['file']

        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
            mimetype_str = m.id_buffer(data.read())
            data.seek(0)

            if mimetype_str in [MIMETYPE_CSV, MIMETYPE_ODS, MIMETYPE_PLAIN]:
                self.filetype = mimetype_str
            else:
                with magic.Magic() as m2:
                    raise forms.ValidationError(
                        code='invalid',
                        message='File "%(filename)s" is of type [%(filetype)s] which is not accepted',
                        params={
                            'filename': data.name,
                            'filetype': m2.id_buffer(data.read())
                        }
                    )
