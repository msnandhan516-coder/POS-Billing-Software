import json
from decimal import Decimal, InvalidOperation

from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from ledger.models import LedgerEntry
from products.models import Product

from .models import Sale, SaleItem


@require_POST
@transaction.atomic
def checkout(request):

    if not request.user.is_authenticated:
        return JsonResponse(
            {
                'success': False,
                'message': 'Authentication required.'
            },
            status=401
        )

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {
                'success': False,
                'message': 'Invalid JSON data.'
            },
            status=400
        )

    items = data.get('items', [])

    if not isinstance(items, list) or not items:
        return JsonResponse(
            {
                'success': False,
                'message': 'Cart cannot be empty.'
            },
            status=400
        )

    payment_method = data.get(
        'payment_method',
        Sale.PaymentMethod.CASH
    )

    customer_name = str(
        data.get('customer_name', '')
    ).strip()

    customer_phone = str(
        data.get('customer_phone', '')
    ).strip()

    notes = str(
        data.get('notes', '')
    ).strip()

    discount_raw = data.get(
        'discount_amount',
        '0'
    )

    valid_payment_methods = {
        Sale.PaymentMethod.CASH,
        Sale.PaymentMethod.CARD,
        Sale.PaymentMethod.UPI,
    }

    if payment_method not in valid_payment_methods:
        return JsonResponse(
            {
                'success': False,
                'message': 'Invalid payment method.'
            },
            status=400
        )

    try:
        discount_amount = Decimal(
            str(discount_raw)
        )
    except (InvalidOperation, TypeError, ValueError):
        return JsonResponse(
            {
                'success': False,
                'message': 'Invalid discount amount.'
            },
            status=400
        )

    if discount_amount < 0:
        return JsonResponse(
            {
                'success': False,
                'message': 'Discount cannot be negative.'
            },
            status=400
        )

    product_ids = []

    for item in items:

        if not isinstance(item, dict):
            return JsonResponse(
                {
                    'success': False,
                    'message': 'Invalid cart item.'
                },
                status=400
            )

        product_id = item.get('product_id')

        if not product_id:
            return JsonResponse(
                {
                    'success': False,
                    'message': 'Each item needs a product_id.'
                },
                status=400
            )

        if product_id in product_ids:
            return JsonResponse(
                {
                    'success': False,
                    'message': (
                        f'Product {product_id} '
                        'appears more than once in the cart.'
                    )
                },
                status=400
            )

        product_ids.append(product_id)

    products = Product.objects.select_for_update().filter(
        id__in=product_ids,
        is_active=True
    )

    products_by_id = {
        product.id: product
        for product in products
    }

    if len(products_by_id) != len(product_ids):

        missing_ids = [
            product_id
            for product_id in product_ids
            if product_id not in products_by_id
        ]

        return JsonResponse(
            {
                'success': False,
                'message': (
                    f'Product(s) not found: {missing_ids}'
                )
            },
            status=404
        )

    cart_items = []

    subtotal = Decimal('0')
    total_tax = Decimal('0')

    for item in items:

        product_id = item.get('product_id')
        quantity_raw = item.get('quantity')

        try:
            quantity = int(quantity_raw)
        except (TypeError, ValueError):
            return JsonResponse(
                {
                    'success': False,
                    'message': (
                        f'Invalid quantity for '
                        f'product {product_id}.'
                    )
                },
                status=400
            )

        if quantity <= 0:
            return JsonResponse(
                {
                    'success': False,
                    'message': (
                        f'Quantity for product '
                        f'{product_id} must be greater than zero.'
                    )
                },
                status=400
            )

        product = products_by_id[product_id]

        if product.stock_quantity < quantity:
            return JsonResponse(
                {
                    'success': False,
                    'message': (
                        f'Insufficient stock for '
                        f'{product.name}. '
                        f'Available: '
                        f'{product.stock_quantity}'
                    )
                },
                status=400
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
        total_tax += item_tax

        cart_items.append(
            {
                'product': product,
                'quantity': quantity,
                'unit_price': unit_price,
                'tax_percentage': product.tax_percentage,
                'subtotal': item_subtotal,
                'tax': item_tax,
                'total': item_total,
            }
        )

    gross_total = subtotal + total_tax

    if discount_amount > gross_total:
        return JsonResponse(
            {
                'success': False,
                'message': (
                    'Discount cannot exceed '
                    'the total amount.'
                )
            },
            status=400
        )

    total_amount = gross_total - discount_amount

    sale = Sale.objects.create(
        staff=request.user,
        customer_name=customer_name,
        customer_phone=customer_phone,
        subtotal=subtotal,
        tax_amount=total_tax,
        discount_amount=discount_amount,
        total_amount=total_amount,
        payment_method=payment_method,
        payment_status=Sale.PaymentStatus.PAID,
        notes=notes,
    )

    for cart_item in cart_items:

        product = cart_item['product']

        if subtotal > 0 and discount_amount > 0:
            item_discount = (
                discount_amount *
                cart_item['subtotal'] /
                subtotal
            )
        else:
            item_discount = Decimal('0')

        item_total = (
            cart_item['total'] -
            item_discount
        )

        SaleItem.objects.create(
            sale=sale,
            product=product,
            quantity=cart_item['quantity'],
            unit_price=cart_item['unit_price'],
            tax_percentage=cart_item['tax_percentage'],
            discount_amount=item_discount,
            subtotal=cart_item['subtotal'],
            total=item_total,
        )

        product.stock_quantity -= cart_item['quantity']

        product.save(
            update_fields=[
                'stock_quantity',
                'updated_at',
            ]
        )

    LedgerEntry.objects.create(
        entry_type=LedgerEntry.EntryType.SALE,
        reference=sale.invoice_number,
        description=f'POS Sale {sale.invoice_number}',
        debit=Decimal('0'),
        credit=total_amount,
        created_by=request.user,
    )

    response_items = []

    for cart_item in cart_items:

        product = cart_item['product']

        response_items.append(
            {
                'product_id': product.id,
                'product_name': product.name,
                'quantity': cart_item['quantity'],
                'unit_price': str(
                    cart_item['unit_price']
                ),
                'tax_percentage': str(
                    cart_item['tax_percentage']
                ),
                'subtotal': str(
                    cart_item['subtotal']
                ),
                'tax': str(
                    cart_item['tax']
                ),
                'remaining_stock': product.stock_quantity,
            }
        )

    return JsonResponse(
        {
            'success': True,
            'message': 'Sale completed successfully.',
            'sale': {
                'invoice_number': sale.invoice_number,
                'customer_name': sale.customer_name,
                'customer_phone': sale.customer_phone,
                'subtotal': str(sale.subtotal),
                'tax_amount': str(sale.tax_amount),
                'discount_amount': str(
                    sale.discount_amount
                ),
                'total_amount': str(
                    sale.total_amount
                ),
                'payment_method': sale.payment_method,
                'payment_status': sale.payment_status,
                'items': response_items,
            }
        },
        status=201
    )