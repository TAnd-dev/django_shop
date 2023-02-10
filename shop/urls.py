from django.urls import path

from shop.views import ProductsList, ItemDetail, ShopCategory, ShopSearch, ShopFavorite, add_favorite, \
    delete_favorite, check_favorite

urlpatterns = [
    path('', ProductsList.as_view(), name='product_list'),
    path('<str:slug>', ShopCategory.as_view(), name='shop_category'),
    path('search/', ShopSearch.as_view(), name='search'),
    path('favorite/', ShopFavorite.as_view(), name='favorite'),
    path('product/<int:pk>/', ItemDetail.as_view(), name='item_detail'),
    path('product/add-favorite/', add_favorite, name='add_favorite'),
    path('product/delete-favorite/', delete_favorite, name='delete_favorite'),
    path('product/check_favorite/<int:item_pk>/', check_favorite, name='check_favorite'),
]
