from django import template

register = template.Library()


@register.filter
def first_name_split(value):
    return value.split()[0]
