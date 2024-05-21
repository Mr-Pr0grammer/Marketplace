from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Product, ProductCart, ProductCartItem


class ProductInline(admin.TabularInline):
    model = Product
    fields = ('name', 'slug', 'quantity', 'price', 'active')
    prepopulated_fields = {'slug': ('name',)}
    show_change_link = True
    extra = 0


class CategoryAdmin(admin.ModelAdmin):
    fields = (('name', 'slug'), ('title', 'description'), 'image')
    list_filter = ('created', 'updated')
    list_display = ('get_image', 'name', 'created', 'updated')
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 50
    inlines = (ProductInline,)
    search_fields = ('name',)
    search_help_text = 'Enter category'
    show_full_result_count = True

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="75">')
        else:
            return '-'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('get_image', 'name', 'category', 'quantity', 'price', 'active', 'created', 'updated')
    list_editable = ('quantity', 'price', 'active')
    list_filter = ('active', 'created', 'updated')
    list_per_page = 50
    search_fields = ('name',)
    search_help_text = 'Enter product name'
    list_display_links = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    fields = (('category', 'active'), ('name', 'slug'), ('quantity', 'price'), ('discount', 'image'), 'short_description', 'long_description')
    show_full_result_count = True

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="75">')
        else:
            return '-'


class ProductCartItemInline(admin.TabularInline):
    model = ProductCartItem
    extra = 0
    show_change_link = True
    fields = ('product', 'quantity')


class ProductCartAdmin(admin.ModelAdmin):
    inlines = (ProductCartItemInline,)
    search_fields = ('user',)
    search_help_text = 'Enter username'
    list_display = ('user',)
    list_display_links = ('user',)
    list_per_page = 50
    show_full_result_count = True


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCart, ProductCartAdmin)