from django import template

register = template.Library()

@register.filter
def get_initials(value):
    words = value.split()
    initials = [words[0][0].upper()]
    if len(words) > 1:
        initials.append(words[-1][0].upper())
    return ''.join()

