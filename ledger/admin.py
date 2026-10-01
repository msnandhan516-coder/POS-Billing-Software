from django.contrib import admin

from .models import LedgerEntry


@admin.register(LedgerEntry)
class LedgerEntryAdmin(admin.ModelAdmin):

    list_display = (
        'entry_type',
        'reference',
        'debit',
        'credit',
        'created_by',
        'created_at',
    )

    list_filter = (
        'entry_type',
        'created_at',
    )

    search_fields = (
        'reference',
        'description',
    )

    readonly_fields = (
        'created_at',
    )