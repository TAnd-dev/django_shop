from django.db.models import QuerySet
from django.db.models import Count, Avg

from shop.models import Item

SORT_ORDER = {
    '1': 'price',
    '2': '-price',
    '3': '-count_purchases',
    '4': '-count_review',
    '5': '-rate'
}


def get_item_filter(request) -> dict:
    try:
        min_price = int(request.GET.get('min_price'))
        min_price = min_price if min_price else 0
    except (ValueError, TypeError):
        min_price = 0
    try:
        max_price = int(request.GET.get('max_price'))
        max_price = max_price if max_price else 999999
    except (ValueError, TypeError):
        max_price = 999999

    sort = request.GET.get('sort')

    return {'min_price': min_price, 'max_price': max_price, 'sort': sort}


def get_items_by_filter(item_filter: dict) -> QuerySet:
    items = Item.objects.filter(price__gte=item_filter.get('min_price'), price__lte=item_filter.get('max_price'))
    sort = item_filter.get('sort')

    if sort == '3':
        items = items.annotate(count_purchases=Count('purchase'))
    elif sort == '4':
        items = items.annotate(count_review=Count('review'))
    elif sort == '5':
        items = items.annotate(rate=Avg('review__rate'))

    return items.order_by(SORT_ORDER.get(item_filter.get('sort'), 'price')).all()


def get_items_by_category(items: QuerySet, category: str) -> QuerySet:
    return items.filter(category__slug=category).all()


def get_search_items(items: QuerySet, search: str) -> QuerySet:
    if search:
        items = items.filter(title__icontains=search).all()
    return items


def get_favorite_items(items: QuerySet, user_id: int) -> QuerySet:
    return items.filter(favorite__user=user_id).all()
