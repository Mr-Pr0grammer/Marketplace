from django.db import models
from django_resized import ResizedImageField
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=110)
    image = ResizedImageField(upload_to='category_pics/', size=[500, 500], blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.name

    def get_image(self):
        # if settings.DEBUG:
        return 'https://bh018dd7r3.execute-api.us-west-2.amazonaws.com' + self.image.url
        # return 'http://127.0.0.1:8000' + self.image.url

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    CHOICE = [
        ('Active', 'active'),
        ('Inactive', 'inactive'),
    ]
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    image = ResizedImageField(upload_to='product_pics/', size=[300, 300], blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, max_length=110)
    price = models.DecimalField(decimal_places=2, verbose_name='Цена', max_digits=10)
    short_description = models.CharField(max_length=255, verbose_name='Краткое описание', default='Тут должно быть описание')
    long_description = models.TextField(verbose_name='Большое описание', default='Тут должно быть описание')
    active = models.CharField(max_length=20, choices=CHOICE, verbose_name='Активность на сайте')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def get_image(self):
        # if settings.DEBUG:
        return 'https://bh018dd7r3.execute-api.us-west-2.amazonaws.com' + self.image.url
        # return 'http://127.0.0.1:8000' + self.image.url

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

