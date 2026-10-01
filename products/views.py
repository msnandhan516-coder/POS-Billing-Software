from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required

from .forms import ProductForm
from .models import Category, Product


@admin_required
def product_list(request):

    search = request.GET.get('search', '').strip()
    category = request.GET.get('category', '').strip()

    products = Product.objects.select_related(
        'category',
        'supplier'
    ).all()

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(sku__icontains=search) |
            Q(barcode__icontains=search)
        )

    if category:
        products = products.filter(
            category_id=category
        )

    paginator = Paginator(products, 10)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    categories = Category.objects.filter(
        is_active=True
    )

    return render(
        request,
        'products/product_list.html',
        {
            'page_obj': page_obj,
            'categories': categories,
            'search': search,
            'selected_category': category,
        }
    )


@admin_required
def product_create(request):

    if request.method == 'POST':
        form = ProductForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            product = form.save()

            messages.success(
                request,
                f'{product.name} created successfully.'
            )

            return redirect('product_list')

    else:
        form = ProductForm()

    return render(
        request,
        'products/product_form.html',
        {
            'form': form,
            'page_title': 'Add Product',
        }
    )


@admin_required
def product_update(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product
        )

        if form.is_valid():

            product = form.save()

            messages.success(
                request,
                f'{product.name} updated successfully.'
            )

            return redirect('product_list')

    else:
        form = ProductForm(
            instance=product
        )

    return render(
        request,
        'products/product_form.html',
        {
            'form': form,
            'page_title': 'Edit Product',
            'product': product,
        }
    )


@admin_required
def product_delete(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    if request.method == 'POST':

        product.is_active = False
        product.save(
            update_fields=['is_active']
        )

        messages.success(
            request,
            f'{product.name} was deactivated.'
        )

    return redirect('product_list')