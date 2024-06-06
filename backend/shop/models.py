from django.contrib.auth.models import User
from django.db import models
from django_resized import ResizedImageField
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=250, blank=True, null=True)
    slug = models.SlugField(unique=True, max_length=110)
    image = ResizedImageField(upload_to='category_pics/', size=[500, 500], blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image.url:
            return 'https://mckuzka.pythonanywhere.com' + self.image.url
        return None

    class Meta:
        verbose_name_plural = 'Categories'


class Product(models.Model):
    CHOICE = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    RATINGS = [
        ('1', '1 star'),
        ('2', '2 stars'),
        ('3', '3 stars'),
        ('4', '4 stars'),
        ('5', '5 stars'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    discount = models.PositiveIntegerField(default=0, verbose_name='Discount %')
    discount_due = models.DateTimeField(default=timezone.now)
    rating = models.CharField(choices=RATINGS, max_length=10, default='1')
    image = ResizedImageField(upload_to='product_pics/', size=[300, 300], blank=True, null=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=110)
    price = models.DecimalField(decimal_places=2, verbose_name='Price $', max_digits=10)
    quantity = models.PositiveIntegerField(default=1)
    short_description = models.CharField(max_length=255, verbose_name='Short description', default='Description')
    long_description = models.TextField(verbose_name='Long description', default='Description')
    active = models.CharField(max_length=20, choices=CHOICE, default='Active')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated at')

    def get_image(self):
        if self.image.url:
            return 'https://mckuzka.pythonanywhere.com' + self.image.url
        return None

    def __str__(self):
        return self.name


class ProductCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'Продуктовая корзина {self.user}'

    class Meta:
        verbose_name = 'User cart'
        verbose_name_plural = 'User carts'


class ProductCartItem(models.Model):
    cart = models.ForeignKey(ProductCart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1,)

    def __str__(self):
        return f'{self.cart.user} - {self.product}'

    class Meta:
        verbose_name = 'Cart item'
        verbose_name_plural = 'Cart items'


class ProductComment(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title[:20]

