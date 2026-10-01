from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def admin_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        if request.user.role != 'ADMIN':
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper


def staff_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect_to_login(request.get_full_path())

        if request.user.role not in ['ADMIN', 'STAFF']:
            raise PermissionDenied

        return view_func(request, *args, **kwargs)

    return wrapper