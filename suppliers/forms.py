from django import forms

from .models import Supplier


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier

        fields = [
            'company_name',
            'contact_person',
            'phone',
            'email',
            'address',
            'is_active',
        ]

        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company name',
            }),

            'contact_person': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact person',
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number',
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email address',
            }),

            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Supplier address',
            }),

            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }