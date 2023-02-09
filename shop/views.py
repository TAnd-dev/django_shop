from django.views.generic import ListView, DetailView

from shop.models import Item


class ProductsList(ListView):
    model = Item
    template_name = 'shop/products.html'
    context_object_name = 'products'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        return Item.objects.all()


class ShopCategory(ListView):
    model = Item
    template_name = 'shop/products.html'
    context_object_name = 'products'
    paginate_by = 10
    allow_empty = True

    def get_queryset(self):
        return Item.objects.filter(category__slug=self.kwargs['slug']).all()

class ItemDetail(DetailView):
    model = Item
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
