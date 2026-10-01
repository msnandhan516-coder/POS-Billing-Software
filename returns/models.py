from django.conf import settings
from django.db import models

from billing.models import Sale, SaleItem
from products.models import Product


class Return(models.Model):

    class Status(models.TextChoices):
        REQUESTED = 'REQUESTED', 'Requested'
        APPROVED = 'APPROVED', 'Approved'
        COMPLETED = 'COMPLETED', 'Completed'
        REJECTED = 'REJECTED', 'Rejected'

    sale = models.ForeignKey(
        Sale,
        on_delete=models.PROTECT,
        related_name='returns'
    )

    sale_item = models.ForeignKey(
        SaleItem,
        on_delete=models.PROTECT,
        related_name='returns'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='returns'
    )

    quantity = models.PositiveIntegerField()

    refund_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.REQUESTED
    )

    processed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='processed_returns',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Return #{self.id} - {self.product.name}"