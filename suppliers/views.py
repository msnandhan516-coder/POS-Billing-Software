from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required

from .forms import SupplierForm
from .models import Supplier


@admin_required
def supplier_list(request):

    search = request.GET.get('search', '').strip()

    suppliers = Supplier.objects.all().order_by(
        'company_name'
    )

    if search:
        suppliers = suppliers.filter(
            Q(company_name__icontains=search) |
            Q(contact_person__icontains=search) |
            Q(phone__icontains=search) |
            Q(email__icontains=search)
        )

    return render(
        request,
        'suppliers/supplier_list.html',
        {
            'suppliers': suppliers,
            'search': search,
        }
    )


@admin_required
def supplier_create(request):

    if request.method == 'POST':

        form = SupplierForm(request.POST)

        if form.is_valid():

            supplier = form.save()

            messages.success(
                request,
                f'Supplier "{supplier.company_name}" created successfully.'
            )

            return redirect('supplier_list')

    else:
        form = SupplierForm()

    return render(
        request,
        'suppliers/supplier_form.html',
        {
            'form': form,
            'page_title': 'Add Supplier',
        }
    )


@admin_required
def supplier_update(request, pk):

    supplier = get_object_or_404(
        Supplier,
        pk=pk
    )

    if request.method == 'POST':

        form = SupplierForm(
            request.POST,
            instance=supplier
        )

        if form.is_valid():

            supplier = form.save()

            messages.success(
                request,
                f'Supplier "{supplier.company_name}" updated successfully.'
            )

            return redirect('supplier_list')

    else:

        form = SupplierForm(
            instance=supplier
        )

    return render(
        request,
        'suppliers/supplier_form.html',
        {
            'form': form,
            'page_title': 'Edit Supplier',
            'supplier': supplier,
        }
    )


@admin_required
def supplier_toggle_status(request, pk):

    supplier = get_object_or_404(
        Supplier,
        pk=pk
    )

    if request.method == 'POST':

        supplier.is_active = not supplier.is_active

        supplier.save(
            update_fields=['is_active']
        )

        status = (
            'activated'
            if supplier.is_active
            else 'deactivated'
        )

        messages.success(
            request,
            f'Supplier "{supplier.company_name}" {status}.'
        )

    return redirect('supplier_list')