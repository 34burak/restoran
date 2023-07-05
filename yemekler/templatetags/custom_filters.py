from django import template
from yemekler.models import Yemek
register = template.Library()

@register.filter
def kategori_display(kategori):
    for choice in Yemek.KATEGORI_CHOICES:
        if choice[0] == kategori:
            return choice[1]
    return ""
