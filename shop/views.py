"""
The necessary imports for the shop view module
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView

from shop.filters import get_item_filter, get_items_by_filter, get_items_by_category, get_search_items, \
    get_favorite_items
from shop.forms import FilterProducts, ReviewForm, PurchaseForm
from shop.models import Item
from shop.sevices import get_items_from_basket, create_purchase, add_review, add_favorite, delete_favorite, \
    check_favorite, add_to_basket, delete_from_basket


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
        return get_item_filter(self.request)

    def get_queryset(self):
        sort = self.get_initial()
        return get_items_by_filter(sort)

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
        return get_items_by_category(items, category=self.kwargs['slug'])


class ShopSearch(BaseShop):
    """
    View filters the items based on a search term
    """

    def get_queryset(self):
        search = self.request.GET.get('s', '')
        items = super().get_queryset()
        return get_search_items(items, search=search)


class ShopFavorite(LoginRequiredMixin, BaseShop):
    """
    View displays the list of favorite items for the logged-in user
    """

    def get_queryset(self):
        items = super().get_queryset()
        return get_favorite_items(items, self.request.user.pk)


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
        return get_items_from_basket(self.request)

    def form_valid(self, form):
        create_purchase(form, self.request)
        self.request.session['basket'] = []
        messages.success(self.request, 'Ваш заказ успешно оформлен!')
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
        add_review(form, self.request.user.id, self.get_object().id)
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER', '/'))


@login_required
def add_favorite_view(request):
    """
    Add an Item to the user's favorite list
    """
    if request.method == 'POST':
        add_favorite(item_id=request.POST.get('item'), user_id=request.user.pk)
        return JsonResponse({'success': True})


@login_required
def delete_favorite_view(request):
    """
    Delete an Item from the user's favorite list
    """
    if request.method == 'POST':
        delete_favorite(item_id=request.POST.get('item'), user_id=request.user.pk)
        return JsonResponse({'success': True})


def check_favorite_view(request, item_pk):
    """
    Check if an Item is in the user's favorite list
    """
    if request.method == 'GET':
        return JsonResponse({'is_favorite': check_favorite(item_pk, request.user.pk)})


def add_to_basket_view(request, item_id=None):
    """
    Add an Item to the user's basket (stored in the session)
    """
    add_to_basket(request, item_id)
    return JsonResponse({'success': True})


def delete_from_basket_view(request):
    """
    Remove an item from the basket (stored in the session)
    """
    delete_from_basket(request)
    return JsonResponse({'success': True})


def check_basket_view(request, item_pk):
    """
    Check if an item is in the basket (stored in the session)
    """
    if request.method == 'GET':
        basket = request.session.get('basket', [])
        in_basket = bool(item_pk in basket)
        return JsonResponse({'in_basket': in_basket})
