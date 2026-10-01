
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Sale


@login_required
def pos(request):
    return render(
        request,
        'billing/pos.html'
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

    sales = Sale.objects.select_related(
        'staff'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'billing/sales_history.html',
        {
            'sales': sales,
        }
    )

