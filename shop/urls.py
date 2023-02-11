from django.urls import path

from shop.views import ProductsList, ItemDetail, ShopCategory, ShopSearch, ShopFavorite, \
    UserBasket, add_favorite, delete_favorite, check_favorite, add_to_basket, \
    delete_from_basket, check_basket, to_basket

urlpatterns = [
    path('', ProductsList.as_view(), name='product_list'),
    path('<str:slug>', ShopCategory.as_view(), name='shop_category'),
    path('search/', ShopSearch.as_view(), name='search'),
    path('favorite/', ShopFavorite.as_view(), name='favorite'),
    path('basket/', UserBasket.as_view(), name='basket'),
    path('product/<int:pk>/', ItemDetail.as_view(), name='item_detail'),
    path('product/add-favorite/', add_favorite, name='add_favorite'),
    path('product/delete-favorite/', delete_favorite, name='delete_favorite'),
    path('product/check-favorite/<int:item_pk>/', check_favorite, name='check_favorite'),
    path('product/add-to-baket', add_to_basket, name='add_to_basket'),
    path('product/basket', to_basket, name='to_basket'),
    path('product/delete-from-baket', delete_from_basket, name='delete_from_basket'),
    path('product/check-basket/<int:item_pk>/', check_basket, name='check_basket'),
]
