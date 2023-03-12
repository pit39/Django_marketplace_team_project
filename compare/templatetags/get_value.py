from django.template import Library


register = Library()


@register.filter(name='get_value')
def get_value(value):
    return round(value, 2)
