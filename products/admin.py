from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'is_active',
        'created_at',
    )

    search_fields = ('name',)

    list_filter = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'sku',
        'category',
        'selling_price',
        'stock_quantity',
        'is_active',
    )

    search_fields = (
        'name',
        'sku',
        'barcode',
    )

    list_filter = (
        'category',
        'is_active',
    )