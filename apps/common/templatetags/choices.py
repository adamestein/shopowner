from django import template

register = template.Library()

@register.filter
def num_choices(form, field):
    # Count the number of iterations and subtract 1 for the empty choice
    return sum(1 for _ in form.fields[field].choices) - 1

