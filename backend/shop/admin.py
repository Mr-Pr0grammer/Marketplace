from django.contrib import admin
from .models import Category, Product


class ProductInline(admin.TabularInline):
    model = Product
    fields = ('name', 'slug', 'price', 'active', 'image')
    prepopulated_fields = {'slug': ('name',)}
    show_change_link = True
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    fields = (('name', 'slug'), 'image')
    list_filter = ('created', 'updated')
    list_display = ('name', 'created', 'updated')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 50
    inlines = (ProductInline,)
    search_fields = ('name',)
    search_help_text = 'Введите категорию'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'active', 'created', 'updated')
    list_editable = ('price', 'active')
    list_filter = ('active', 'created', 'updated')
    list_per_page = 50
    search_fields = ('name',)
    search_help_text = 'Введите название товара'
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    fields = (('category', 'active'), ('name', 'slug'), ('short_description', 'price'), 'image', 'long_description')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)

