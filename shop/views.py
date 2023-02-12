"""
The necessary imports for the shop view module
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Avg, Sum
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView

from shop.forms import FilterProducts, ReviewForm, PurchaseForm
from shop.models import Item, Favorite
from users.models import CustomUser


class BaseShop(ListView, FormView):
    """
    The base view for other list views
    """
    model = Item
    template_name = 'shop/products.html'
    context_object_name = 'products'
    paginate_by = 10
    allow_empty = True
    form_class = FilterProducts

    def get_initial(self):
        try:
            min_price = int(self.request.GET.get('min_price'))
            min_price = min_price if min_price else 0
        except (ValueError, TypeError):
            min_price = 0
        try:
            max_price = int(self.request.GET.get('max_price'))
            max_price = max_price if max_price else 999999
        except (ValueError, TypeError):
            max_price = 999999

        sort = self.request.GET.get('sort')
        return {'min_price': min_price, 'max_price': max_price, 'sort': sort}

    def get_queryset(self):
        sort = self.get_initial()
        items = Item.objects.filter(price__gte=sort['min_price'], price__lte=sort['max_price'])

        if sort['sort'] == '1':
            items = items.order_by('price').all()
        elif sort['sort'] == '2':
            items = items.order_by('-price').all()
        elif sort['sort'] == '3':
            items = items.annotate(count_purchases=Count('purchase')).order_by(
                '-count_purchases').all()
        elif sort['sort'] == '4':
            items = items.annotate(count_review=Count('review')).order_by('-count_review').all()
        elif sort['sort'] == '5':
            items = items.annotate(rate=Avg('review__rate')).order_by('-rate').all()

        return items

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        params = self.request.GET.items()
        params_str = ''.join([f'&{key}={value}' for key, value in params if key != 'page'])
        context['params'] = params_str
        return context


class ProductsList(BaseShop):
    """
    View displays the entire list of items for sale
    """


class ShopCategory(BaseShop):
    """
    View filters the items based on a specific category
    """

    def get_queryset(self):
        items = super().get_queryset()
        return items.filter(category__slug=self.kwargs['slug']).all()


class ShopSearch(BaseShop):
    """
    View filters the items based on a search term
    """

    def get_queryset(self):
        search = self.request.GET.get('s')
        items = super().get_queryset()
        if search:
            items = items.filter(title__icontains=search).all()
        return items


class ShopFavorite(LoginRequiredMixin, BaseShop):
    """
    View displays the list of favorite items for the logged-in user
    """

    def get_queryset(self):
        items = super().get_queryset()
        return items.filter(favorite__user=self.request.user.pk).all()


class UserBasket(CreateView, ListView):
    """
    View displays the items in the user's basket and allows the user to purchase it
    """
    model = Item
    template_name = 'shop/basket.html'
    context_object_name = 'products'
    allow_empty = True

    form_class = PurchaseForm
    success_url = reverse_lazy('basket')

    def get_queryset(self):
        basket = self.request.session.get('basket', [])
        return Item.objects.filter(pk__in=basket).all()

    def form_valid(self, form):
        purchase = form.save(commit=False)

        products = self.get_queryset()
        total_price = products.aggregate(Sum('price')).get('price__sum')
        user = self.request.user
        user = user if user.pk else None

        purchase.total_price = total_price
        purchase.user = user
        purchase = form.save()
        purchase.item.add(*products)

        messages.success(self.request, 'Ваш заказ успешно оформлен!')
        self.request.session['basket'] = []
        return super().form_valid(form)


class ItemDetail(DetailView, CreateView):
    """
    View for a specific Item instance with adding a review for the item
    """
    model = Item
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    form_class = ReviewForm

    def form_invalid(self, form):
        messages.error(self.request, 'Ошибка при добавлении комментария')
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))

    def form_valid(self, form):
        review = form.save(commit=False)
        review.author_id = self.request.user.id
        review.product_id = self.get_object().id
        review.save()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))


@login_required
def add_favorite(request):
    """
    Add an Item to the user's favorite list
    """
    if request.method == 'POST':
        item = Item.objects.get(pk=request.POST.get('item'))
        user = CustomUser.objects.get(pk=request.user.pk)
        Favorite.objects.create(user=user, item=item)
        return JsonResponse({'success': True})


@login_required
def delete_favorite(request):
    """
    Delete an Item from the user's favorite list
    """
    if request.method == 'POST':
        item = Item.objects.get(pk=request.POST.get('item'))
        user = CustomUser.objects.get(pk=request.user.pk)
        Favorite.objects.get(user=user, item=item).delete()
        return JsonResponse({'success': True})


def check_favorite(request, item_pk):
    """
    Check if an Item is in the user's favorite list
    """
    if request.method == 'GET':
        user_id = request.user.pk
        is_favorite = bool(Favorite.objects.filter(user__pk=user_id, item__id=item_pk))
        return JsonResponse({'is_favorite': is_favorite})


def add_to_basket(request, item_id=None):
    """
    Add an Item to the user's basket (stored in the session)
    """
    if request.method == 'POST':
        item_id = int(request.POST.get('item'))

    basket = request.session.get('basket', [])

    if item_id not in basket:
        basket.append(item_id)

    request.session['basket'] = basket
    return JsonResponse({'success': True})


def delete_from_basket(request):
    """
    Remove an item from the basket (stored in the session)
    """
    if request.method == 'POST':
        item_id = int(request.POST.get('item'))
        basket = request.session.get('basket', [])

        if item_id in basket:
            basket.remove(item_id)

        request.session['basket'] = basket
        return JsonResponse({'success': True})


def check_basket(request, item_pk):
    """
    Check if an item is in the basket (stored in the session)
    """
    if request.method == 'GET':
        basket = request.session.get('basket', [])
        in_basket = bool(item_pk in basket)
        return JsonResponse({'in_basket': in_basket})


def to_basket(request):
    """
    Add an item to the basket (stored in the session)
    """
    if request.method == 'POST':
        item_id = int(request.POST.get('item'))
        add_to_basket(request, item_id)
    return reverse_lazy('basket')
