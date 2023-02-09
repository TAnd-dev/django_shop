from django import template

from shop.models import Category

register = template.Library()


@register.inclusion_tag('categories_menu.html')
def show_categories():
    categories = Category.objects.all()
    return {'categories': categories}
