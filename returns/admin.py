from django.contrib import admin

from .models import Return


@admin.register(Return)
class ReturnAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'sale',
        'product',
        'quantity',
        'refund_amount',
        'status',
        'created_at',
    )

    search_fields = (
        'sale__invoice_number',
        'product__name',
    )

    list_filter = (
        'status',
        'created_at',
    )