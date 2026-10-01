from decimal import Decimal

from django.db import transaction
from django.core.exceptions import ValidationError

from billing.models import Sale, SaleItem
from ledger.models import LedgerEntry
from products.models import Product


@transaction.atomic
def create_sale(
    *,
    staff,
    cart_items,
    payment_method,
    customer_name='',
    customer_phone='',
    discount_amount=Decimal('0'),
    notes=''
):
    """
    Create a complete POS sale atomically.

    cart_items format:

    [
        {
            'product_id': 1,
            'quantity': 2,
        },
        ...
    ]
    """

    if not cart_items:
        raise ValidationError("Cart cannot be empty.")

    subtotal = Decimal('0')
    tax_amount = Decimal('0')
    sale_items = []

    # Validate products and calculate totals first
    for item in cart_items:

        product_id = item.get('product_id')
        quantity = int(item.get('quantity', 0))

        if quantity <= 0:
            raise ValidationError(
                "Product quantity must be greater than zero."
            )

        product = Product.objects.select_for_update().get(
            id=product_id,
            is_active=True
        )

        if product.stock_quantity < quantity:
            raise ValidationError(
                f"Insufficient stock for {product.name}. "
                f"Available: {product.stock_quantity}"
            )

        unit_price = product.selling_price

        item_subtotal = unit_price * quantity

        item_tax = (
            item_subtotal *
            product.tax_percentage /
            Decimal('100')
        )

        item_total = item_subtotal + item_tax

        subtotal += item_subtotal
        tax_amount += item_tax

        sale_items.append({
            'product': product,
            'quantity': quantity,
            'unit_price': unit_price,
            'tax_percentage': product.tax_percentage,
            'subtotal': item_subtotal,
            'total': item_total,
        })

    discount_amount = Decimal(discount_amount)

    if discount_amount < 0:
        raise ValidationError(
            "Discount cannot be negative."
        )

    gross_total = subtotal + tax_amount

    if discount_amount > gross_total:
        raise ValidationError(
            "Discount cannot exceed the total amount."
        )

    total_amount = gross_total - discount_amount

    # Create sale
    sale = Sale.objects.create(
        staff=staff,
        customer_name=customer_name,
        customer_phone=customer_phone,
        subtotal=subtotal,
        tax_amount=tax_amount,
        discount_amount=discount_amount,
        total_amount=total_amount,
        payment_method=payment_method,
        payment_status=Sale.PaymentStatus.PAID,
        notes=notes,
    )

    # Create sale items + reduce stock
    for item in sale_items:

        product = item['product']

        SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=item['quantity'],
            unit_price=item['unit_price'],
            tax_percentage=item['tax_percentage'],
            subtotal=item['subtotal'],
            total=item['total'],
        )

        product.stock_quantity -= item['quantity']
        product.save(update_fields=['stock_quantity'])

    # Create ledger entry
    LedgerEntry.objects.create(
        entry_type=LedgerEntry.EntryType.SALE,
        reference=sale.invoice_number,
        description=(
            f"POS Sale {sale.invoice_number}"
        ),
        debit=Decimal('0'),
        credit=total_amount,
        created_by=staff,
    )

    return sale