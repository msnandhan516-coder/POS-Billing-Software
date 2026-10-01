from django.contrib import admin

from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = (
        'subtotal',
        'total',
    )


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):

    list_display = (
        'invoice_number',
        'staff',
        'total_amount',
        'payment_method',
        'payment_status',
        'created_at',
    )

    search_fields = (
        'invoice_number',
        'customer_name',
        'customer_phone',
    )

    list_filter = (
        'payment_method',
        'payment_status',
        'created_at',
    )

    readonly_fields = (
        'invoice_number',
        'subtotal',
        'tax_amount',
        'total_amount',
        'created_at',
        'updated_at',
    )

    inlines = [SaleItemInline]