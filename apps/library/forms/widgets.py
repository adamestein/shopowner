from itertools import cycle
from os.path import join
import re

from django import forms
from django.conf import settings
from django.forms import DateInput, Widget
from django.utils.safestring import mark_safe

DEFAULT_ONCLICK = "return showAddAnotherPopup(this);"
DEFAULT_URL = '/admin/%(app_label)s/%(model_name)s/add/?_to_field=id&_popup=1'


class HTML5DateInput(DateInput):
    input_type = 'date'


class InlineFormset(Widget):
    def __init__(self, formset, attrs=None, form_kwargs=None):
        super().__init__(attrs)
        self.delete_icon = join(settings.STATIC_URL, 'img', 'delete.png')
        self.formset_class = formset
        self.form_kwargs = form_kwargs or {}
        self.instance = self.form_kwargs.pop('instance', None)

    def value_from_datadict(self, data, files, name):
        formset = self.formset_class(data, files, instance=self.instance)
        if formset.is_valid():
            ret_value = formset
        else:
            ret_value = None

        return ret_value

    def render(self, name, value, attrs=None, renderer=None):
        add_icon = join(settings.STATIC_URL, 'img', 'add.png')
        formset = self.formset_class(instance=self.instance, form_kwargs=self.form_kwargs)

        data_html = ''
        header_html = ''

        field_names = formset.form.base_fields.keys()

        for field in field_names:
            header_html += f'<th style="width: 45%;">{field.capitalize()}</th>'
        header_html += '<th style="font-weight: normal !important; text-align: center;">Delete?</th>'

        row_iter = cycle(range(1, 3))
        for form in formset:
            data_html += f'''
                <tr class="row{next(row_iter)}">
                    {self._cells(form)}
                </tr>
            '''

        # The empty help-block paragraph is used to get the standard spacing between this and the next widget. The
        # <table></table> tags around the empty form row is so that all the <tr> and <td> tags show up correctly
        # (without <table></table>, those tags disappear).
        return mark_safe(f'''
            {formset.management_form}
                        
            <div id="forset_table_empty_form" style="display: none;">
                <table><tr>{self._cells(formset.empty_form, empty_form=True)}</tr></table>
            </div>
            
            <table class="formset_table table" id="{attrs["id"] + "_table"}">
                <tr>{header_html}</tr>
                
                {data_html}

                <tr class="add-row">
                    <td colspan="{len(field_names) + int(formset.can_delete)}">
                        <img src="{add_icon}" />
                        <a id="add_item">Add another item</a>
                    </td>
                </tr>
            </table>
            
            <p class="help-block"></p>
            
            <script>
                if ($ === undefined) {{
                    $ = django.jQuery;
                }}
                
                $(".add-row").click(function() {{
                    let form_idx = parseInt($("#id_{formset.prefix}-TOTAL_FORMS").val());
                    let cells = $("#forset_table_empty_form tr").html();
                    let rowColor = (form_idx % 2 === 0) ? "row1" : "row2";
                    let row = `<tr class="${{rowColor}}">${{cells}}</tr>`;
                    
                    $("#{attrs["id"] + "_table"} tr:last").before(row.replace(/__prefix__/g, form_idx));
                    $("#id_{formset.prefix}-TOTAL_FORMS").val(form_idx + 1);
                }});
                
                $(".formset_table").on("click", ".delete-row", function() {{
                    $(this).closest("tr").remove();
                }});
            </script>
        ''')

    def _cells(self, form, empty_form=False):
        html = ''

        for field in form:
            if not field.is_hidden and (not empty_form or 'DELETE' not in field.auto_id):
                html += f'<td>{field}</td>'
            else:
                html += str(field)

        if empty_form:
            html += f'<td class="delete-row"><img class="delete_icon" src="{self.delete_icon}"></td>'

        return html


class SelectWithAdd(forms.Select):
    def __init__(self, fk_field, attrs=None, choices=(), parameters=None):
        super().__init__(attrs, choices)
        self.popup_add = self._create_popup_anchor(fk_field, parameters)

    def render(self, name, value, attrs=None, renderer=None):
        field_name = re.sub(r'.*-(\d+|__prefix__)-', '', name)

        html = super().render(name, value, attrs, renderer)
        return mark_safe(
            html + self.popup_add % {
                'field': field_name.replace('_', ''),
                'id_name': name,
                'name': name.replace('_', ' '),
                'static_url': settings.STATIC_URL
            }
        )

    @staticmethod
    def _create_popup_anchor(fk_field, parameters):
        onclick = DEFAULT_ONCLICK
        # noinspection PyProtectedMember
        rel = fk_field.field.related_model._meta
        url = DEFAULT_URL % {'app_label': rel.app_label, 'model_name': rel.model_name}

        if parameters:
            for key, value in parameters.items():
                url += f'&{key}={value}'

        anchor = f"""
            <a href="{url}" class="add-another" id="add_id_%(id_name)s" onclick="{onclick}"
               title="Add another %(name)s">
                <img src="%(static_url)simg/icon-addlink.svg" alt="Add">
            </a>
        """

        return anchor


class SelectMultipleWithAdd(forms.SelectMultiple, SelectWithAdd):
    pass
