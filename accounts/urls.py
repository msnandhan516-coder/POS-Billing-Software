from django.urls import path

from .views import (
    login_view,
    logout_view,
    staff_create,
    staff_list,
    staff_toggle_status,
)


urlpatterns = [

    path(
        'login/',
        login_view,
        name='login'
    ),

    path(
        'logout/',
        logout_view,
        name='logout'
    ),

    path(
        'staff/',
        staff_list,
        name='staff_list'
    ),

    path(
        'staff/add/',
        staff_create,
        name='staff_create'
    ),

    path(
        'staff/<int:pk>/toggle/',
        staff_toggle_status,
        name='staff_toggle_status'
    ),
]