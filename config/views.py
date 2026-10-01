from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from django.utils import timezone

from accounts.decorators import admin_required
from accounts.models import User
from billing.models import Sale
from products.models import Product


@login_required
@admin_required
def admin_dashboard(request):

    today = timezone.localdate()

    today_sales = Sale.objects.filter(
        created_at__date=today,
        payment_status=Sale.PaymentStatus.PAID
    )

    context = {
        'total_products': Product.objects.filter(
            is_active=True
        ).count(),

        'low_stock_products': Product.objects.filter(
            is_active=True,
            stock_quantity__lte=5
        ).count(),

        'total_staff': User.objects.filter(
            role=User.Role.STAFF,
            is_active=True
        ).count(),

        'today_transactions': today_sales.count(),

        'today_sales': today_sales.aggregate(
            total=Sum('total_amount')
        )['total'] or 0,
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

    response = render(
        request,
        'billing/dashboard.html'
    )


    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response