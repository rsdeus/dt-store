from django.template import Library

register = Library()


@register.simple_tag(name='calculate_total_per_product')
def calculate_total_per_product(arg1, arg2):
    try:
        total = arg1 * arg2
    except:
        total = 0
    return total
