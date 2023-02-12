from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey, TreeManyToManyField

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg
from django.db import models
from django.urls import reverse

from django_shop import settings


class Category(MPTTModel):
    name = models.CharField(
        max_length=32,
        verbose_name='Name',
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
    )
    slug = models.SlugField(
        max_length=40,
        verbose_name='url',
        unique=True,
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('shop_category', kwargs={'slug': self.slug})


class Item(models.Model):
    title = models.CharField(
        max_length=124,
        verbose_name='Title'
    )
    category = TreeManyToManyField(
        Category,
        verbose_name='Category',
        related_name='category',
    )
    description = models.TextField(
        verbose_name='Description'
    )
    price = models.DecimalField(
        verbose_name='Price',
        max_digits=8,
        decimal_places=2,
        default=0
    )
    salesman = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='items',
        verbose_name='salesman',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(
        verbose_name='Created',
        auto_now_add=True
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk': self.pk})

    def get_avg_rate(self):
        return Review.objects.filter(product=self).aggregate(Avg('rate'))['rate__avg']


class ProductGallery(models.Model):
    image = models.ImageField(
        upload_to='gallery_product',
        verbose_name='Image'
    )
    product = models.ForeignKey(
        Item,
        related_name='image',
        verbose_name='Product',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.product}'


class Review(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='review',
        verbose_name='Author',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Item,
        related_name='review',
        verbose_name='Product',
        on_delete=models.CASCADE
    )
    text = models.TextField(
        verbose_name='text'
    )
    rate = models.SmallIntegerField(
        verbose_name='Rate',
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ]
    )
    created_at = models.DateTimeField(
        verbose_name='created',
        auto_now_add=True
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.product}'


class Favorite(models.Model):
    item = models.ForeignKey(
        Item,
        related_name='favorite',
        verbose_name='Item',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='favorite',
        verbose_name='User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.item}'


class Purchase(models.Model):
    item = models.ManyToManyField(
        Item,
        related_name='purchase',
        verbose_name='Item',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=None,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    is_delivery = models.BooleanField(
        verbose_name='Is Delivery',
    )
    total_price = models.DecimalField(
        verbose_name='Total price',
        max_digits=12,
        decimal_places=2
    )
    created_at = models.DateTimeField(
        verbose_name='Created at',
        auto_now_add=True,
    )
    email = models.EmailField(
        verbose_name='Email',
    )
    phone = models.BigIntegerField(
        verbose_name='Phone',
        null=True,
        blank=True
    )
    country = models.CharField(
        max_length=64,
        verbose_name='Country',
        null=True,
        blank=True
    )
    city = models.CharField(
        max_length=24,
        verbose_name='City',
        null=True,
        blank=True
    )
    street = models.CharField(
        max_length=128,
        verbose_name='Street',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f'{self.email}'
