from django.urls import path

from shop.views import ProductsList, ItemDetail, ShopCategory

urlpatterns = [
    path('', ProductsList.as_view(), name='product_list'),
    path('<str:slug>', ShopCategory.as_view(), name='shop_category'),
    path('product/<int:pk>', ItemDetail.as_view(), name='item_detail'),
]
