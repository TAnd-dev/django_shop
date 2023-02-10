from django.contrib import messages
from django.db.models import Count, Avg
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, FormView, CreateView

from shop.forms import FilterProducts, ReviewForm
from shop.models import Item


class BaseShop(ListView, FormView):
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
        # elif sort['sort'] == '3':
        elif sort['sort'] == '4':
            items = items.annotate(count_review=Count('review')).order_by('-count_review').all()
        elif sort['sort'] == '5':
            items = items.annotate(rate=Avg('review__rate')).order_by('-rate').all()

        return items


class ProductsList(BaseShop):
    pass


class ShopCategory(BaseShop):
    def get_queryset(self):
        items = super().get_queryset()
        return items.filter(category__slug=self.kwargs['slug']).all()


class ItemDetail(DetailView, CreateView):
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
