from django import template

register = template.Library()  # Correct method for creating a Library instance

@register.filter(name='range_filter')
def range_filter(value):
    return value[:500] + "..........."
