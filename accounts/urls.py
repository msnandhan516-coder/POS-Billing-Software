from django.contrib.auth.views import redirect_to_login
from django.urls import path
from django.views.generic import RedirectView

from .views import (
    login_view,
    logout_view,
    staff_create,
    staff_list,
    staff_toggle_status,
)


urlpatterns = [

    # Redirect bare root → login page
    path(
        '',
        RedirectView.as_view(url='/login/', permanent=False),
        name='home'
    ),


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