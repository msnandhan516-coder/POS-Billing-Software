from django.conf import settings
from django.db import models


class LedgerEntry(models.Model):

    class EntryType(models.TextChoices):
        SALE = 'SALE', 'Sale'
        RETURN = 'RETURN', 'Return'
        EXPENSE = 'EXPENSE', 'Expense'
        ADJUSTMENT = 'ADJUSTMENT', 'Adjustment'

    entry_type = models.CharField(
        max_length=20,
        choices=EntryType.choices
    )

    reference = models.CharField(
        max_length=100,
        blank=True
    )

    description = models.TextField()

    debit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    credit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.entry_type} - {self.description}"    