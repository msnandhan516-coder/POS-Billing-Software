
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from django.shortcuts import get_object_or_404

from accounts.decorators import admin_required

from .forms import *
from .models import User


def redirect_by_role(user):

    if user.role == User.Role.ADMIN:
        return redirect('admin_dashboard')

    if user.role == User.Role.STAFF:
        return redirect('pos')

    logout(user)

    return redirect('login')


def login_view(request):

    if request.user.is_authenticated:
        return redirect_by_role(request.user)

    form = LoginForm(
        request,
        data=request.POST or None
    )

    if request.method == 'POST' and form.is_valid():

        user = form.get_user()

        if not user.is_active:

            form.add_error(
                None,
                'Your account is inactive.'
            )

        else:

            login(request, user)

            return redirect_by_role(user)

    return render(
        request,
        'accounts/login.html',
        {
            'form': form
        }
    )


@login_required
def logout_view(request):

    logout(request)

    response = HttpResponseRedirect('/login/')

    response['Cache-Control'] = (
        'no-cache, no-store, must-revalidate'
    )

    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response


@admin_required
def staff_list(request):

    staff_members = User.objects.filter(
        role=User.Role.STAFF
    ).order_by(
        '-date_joined'
    )

    return render(
        request,
        'accounts/staff_list.html',
        {
            'staff_members': staff_members,
        }
    )


@admin_required
def staff_create(request):

    if request.method == 'POST':

        form = StaffCreateForm(
            request.POST
        )

        if form.is_valid():

            staff = form.save()

            messages.success(
                request,
                f'Staff account "{staff.username}" created successfully.'
            )

            return redirect('staff_list')

    else:

        form = StaffCreateForm()

    return render(
        request,
        'accounts/staff_form.html',
        {
            'form': form,
            'page_title': 'Add Staff',
        }
    )


@admin_required
def staff_toggle_status(request, pk):

    staff = get_object_or_404(
        User,
        pk=pk,
        role=User.Role.STAFF
    )

    if request.method == 'POST':

        staff.is_active = not staff.is_active

        staff.save(
            update_fields=['is_active']
        )

        status = (
            'activated'
            if staff.is_active
            else 'deactivated'
        )

        messages.success(
            request,
            f'Staff "{staff.username}" {status}.'
        )

    return redirect('staff_list')

