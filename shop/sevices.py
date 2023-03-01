from django.db.models import Sum, QuerySet

from shop.forms import PurchaseForm, ReviewForm
from shop.models import Item, Favorite
from users.models import CustomUser


def get_items_by_list_ids(ids: list):
    return Item.objects.filter(pk__in=ids).all()


def get_items_from_basket(request) -> QuerySet:
    item_ids = request.session.get('basket', [])
    return get_items_by_list_ids(item_ids)


def get_sum_of_products(products: QuerySet) -> int:
    return products.aggregate(Sum('price')).get('price__sum')


def create_purchase(form: PurchaseForm, request) -> None:
    purchase = form.save(commit=False)
    products = get_items_from_basket(request)
    total_price = get_sum_of_products(products)
    user = request.user
    user = user if user.pk else None

    purchase.total_price = total_price
    purchase.user = user
    purchase = form.save()
    purchase.item.add(*products)


def add_review(form: ReviewForm, user_id: int, item_id: int) -> None:
    review = form.save(commit=False)
    review.author_id = user_id
    review.product_id = item_id
    review.save()


def add_favorite(item_id: int, user_id: int) -> None:
    item = Item.objects.get(pk=item_id)
    user = CustomUser.objects.get(pk=user_id)
    Favorite.objects.create(user=user, item=item)


def delete_favorite(item_id: int, user_id: int) -> None:
    item = Item.objects.get(pk=item_id)
    user = CustomUser.objects.get(pk=user_id)
    Favorite.objects.get(user=user, item=item).delete()


def check_favorite(item_id: int, user_id: int) -> bool:
    return bool(Favorite.objects.filter(user__pk=user_id, item__id=item_id))


def add_to_basket(request, item_id) -> None:
    if request.method == 'POST':
        item_id = int(request.POST.get('item'))

    basket = request.session.get('basket', [])

    if item_id not in basket:
        basket.append(item_id)

    request.session['basket'] = basket


def delete_from_basket(request) -> None:
    if request.method == 'POST':
        item_id = int(request.POST.get('item'))
        basket = request.session.get('basket', [])

        if item_id in basket:
            basket.remove(item_id)

        request.session['basket'] = basket
