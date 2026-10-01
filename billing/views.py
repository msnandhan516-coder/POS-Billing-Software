from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q, Sum
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from products.models import Category, Product
from .models import Sale


@login_required
def pos(request):
    products = Product.objects.filter(is_active=True).select_related('category')
    categories = Category.objects.filter(is_active=True)

    last_sale = Sale.objects.order_by('-id').first()
    next_number = (last_sale.id + 1) if last_sale else 1
    next_invoice_number = f"INV-{next_number:06d}"

    return render(
        request,
        'billing/pos.html',
        {
            'products': products,
            'categories': categories,
            'next_invoice_number': next_invoice_number,
        }
    )


@login_required
def invoice(request, invoice_number):
    sale = get_object_or_404(
        Sale.objects.prefetch_related(
            'items__product'
        ),
        invoice_number=invoice_number
    )

    return render(
        request,
        'billing/invoice.html',
        {
            'sale': sale,
        }
    )


@login_required
def sales_history(request):
    search = request.GET.get('search', '').strip()
    payment_method = request.GET.get('payment_method', '').strip()

    sales = Sale.objects.select_related('staff').order_by('-created_at')

    if search:
        sales = sales.filter(
            Q(invoice_number__icontains=search) |
            Q(customer_name__icontains=search) |
            Q(customer_phone__icontains=search) |
            Q(staff__username__icontains=search)
        )

    if payment_method:
        sales = sales.filter(payment_method=payment_method)

    # Calculate KPIs
    today = timezone.localdate()
    today_sales = Sale.objects.filter(
        created_at__date=today,
        payment_status=Sale.PaymentStatus.PAID
    )
    today_revenue = today_sales.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    total_transactions = Sale.objects.count()
    avg_order_value = Sale.objects.filter(payment_status=Sale.PaymentStatus.PAID).aggregate(avg=Avg('total_amount'))['avg'] or Decimal('0.00')

    return render(
        request,
        'billing/sales_history.html',
        {
            'sales': sales,
            'search': search,
            'payment_method': payment_method,
            'today_revenue': today_revenue,
            'total_transactions': total_transactions,
            'avg_order_value': avg_order_value,
        }
    )
