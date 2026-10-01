from django import forms

from .models import Category, Product


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            'name',
            'description',
            'is_active',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category name',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Category description',
            }),

            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            'name',
            'sku',
            'barcode',
            'category',
            'supplier',
            'description',
            'purchase_price',
            'selling_price',
            'tax_percentage',
            'stock_quantity',
            'minimum_stock',
            'image',
            'is_active',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Product name',
            }),

            'sku': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'SKU',
            }),

            'barcode': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Barcode',
            }),

            'category': forms.Select(attrs={
                'class': 'form-select',
            }),

            'supplier': forms.Select(attrs={
                'class': 'form-select',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),

            'purchase_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
            }),

            'selling_price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
            }),

            'tax_percentage': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
            }),

            'stock_quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),

            'minimum_stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),

            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        purchase_price = cleaned_data.get('purchase_price')
        selling_price = cleaned_data.get('selling_price')

        if (
            purchase_price is not None
            and selling_price is not None
            and selling_price < purchase_price
        ):
            self.add_error(
                'selling_price',
                'Selling price cannot be lower than purchase price.'
            )

        return cleaned_data