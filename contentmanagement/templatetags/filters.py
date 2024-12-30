from django import template

register = template.Library()


@register.filter
def enumerate_queryset(queryset):
    return enumerate(queryset)


@register.filter
def letter(value, start_letter="A"):
    return chr(ord(start_letter) + value)
