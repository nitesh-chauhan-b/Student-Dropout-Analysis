from django import template

register = template.Library()

@register.filter(name='dict_lookup')
def dict_lookup(dictionary, key):
    try:
        return dictionary[key]
    except KeyError:
        return None


@register.filter
def get_year_range():
    return range(2000, 2024)