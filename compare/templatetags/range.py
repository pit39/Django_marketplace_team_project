from django.template import Library


register = Library()


@register.filter(name='range_number')
def range_number(value):
    return range(value)
