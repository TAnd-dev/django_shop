from django.contrib import admin

from shop.models import Item, Category, Review, ProductGallery, Favorite


class Gallery(admin.TabularInline):
    fk_name = 'product'
    model = ProductGallery


class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    inlines = [Gallery, ]


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review)
admin.site.register(Favorite)
