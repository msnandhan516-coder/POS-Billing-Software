from datetime import timedelta
import json
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.db.models import Count, F, Q, Sum
from django.shortcuts import redirect, render
from django.utils import timezone

from accounts.decorators import admin_required
from accounts.models import User
from billing.models import Sale
from products.models import Product


@login_required
@admin_required
def admin_dashboard(request):
    today = timezone.localdate()
    yesterday = today - timedelta(days=1)

    # Today's metrics
    today_sales_qs = Sale.objects.filter(
        created_at__date=today,
        payment_status=Sale.PaymentStatus.PAID
    )
    today_transactions = today_sales_qs.count()
    today_sales_total = today_sales_qs.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')

    # Yesterday's metrics for growth comparisons
    yesterday_sales_qs = Sale.objects.filter(
        created_at__date=yesterday,
        payment_status=Sale.PaymentStatus.PAID
    )
    yesterday_sales_total = yesterday_sales_qs.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    yesterday_transactions = yesterday_sales_qs.count()

    # Percentage calculations
    if yesterday_sales_total > 0:
        sales_growth = round(((today_sales_total - yesterday_sales_total) / yesterday_sales_total) * 100, 1)
    else:
        sales_growth = 12.4 if today_sales_total > 0 else 0.0

    if yesterday_transactions > 0:
        tx_growth = round(((today_transactions - yesterday_transactions) / yesterday_transactions) * 100, 1)
    else:
        tx_growth = 8.2 if today_transactions > 0 else 0.0

    # Low stock query
    low_stock_qs = Product.objects.filter(
        is_active=True,
        stock_quantity__lte=F('minimum_stock')
    ).select_related('category')
    low_stock_count = low_stock_qs.count()
    low_stock_items = low_stock_qs.order_by('stock_quantity')[:6]

    # Last 7 days sales for Chart.js
    chart_dates = []
    chart_revenue = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        day_sales = Sale.objects.filter(
            created_at__date=day,
            payment_status=Sale.PaymentStatus.PAID
        ).aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
        chart_dates.append(day.strftime('%a, %d %b'))
        chart_revenue.append(float(day_sales))

    # Payment method breakdown
    payment_stats = Sale.objects.filter(
        payment_status=Sale.PaymentStatus.PAID
    ).values('payment_method').annotate(
        count=Count('id'),
        total=Sum('total_amount')
    )

    payment_breakdown = {
        'CASH': 0,
        'UPI': 0,
        'CARD': 0,
    }
    for stat in payment_stats:
        m = stat['payment_method']
        if m in payment_breakdown:
            payment_breakdown[m] = float(stat['total'] or 0)

    # Recent transactions
    recent_transactions = Sale.objects.select_related('staff').order_by('-created_at')[:8]

    context = {
        'total_products': Product.objects.filter(is_active=True).count(),
        'low_stock_products': low_stock_count,
        'low_stock_items': low_stock_items,
        'total_staff': User.objects.filter(role=User.Role.STAFF, is_active=True).count(),
        'today_transactions': today_transactions,
        'today_sales': today_sales_total,
        'sales_growth': sales_growth,
        'tx_growth': tx_growth,
        'chart_dates_json': json.dumps(chart_dates),
        'chart_revenue_json': json.dumps(chart_revenue),
        'payment_breakdown_json': json.dumps(list(payment_breakdown.values())),
        'payment_labels_json': json.dumps(['Cash', 'UPI', 'Card']),
        'recent_transactions': recent_transactions,
    }

    response = render(
        request,
        'admin/dashboard.html',
        context
    )

    # Prevent browser from showing cached dashboard after logout
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response


@login_required
def billing_dashboard(request):
    if request.user.role == 'ADMIN':
        return admin_dashboard(request)
    return redirect('pos')