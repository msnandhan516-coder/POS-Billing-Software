from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autocomplete': 'username',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete': 'current-password',
        })
    )


class StaffCreateForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password',
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.STAFF
        user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()

        return user


from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
            'autocomplete': 'username',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'autocomplete': 'current-password',
        })
    )


class StaffCreateForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'password',
        ]

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),

            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),

            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }

    def save(self, commit=True):

        user = super().save(commit=False)

        user.role = User.Role.STAFF

        user.set_password(
            self.cleaned_data['password']
        )

        if commit:
            user.save()

        return user    


