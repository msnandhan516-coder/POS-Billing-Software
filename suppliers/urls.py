from django.urls import path

from .views import (
    supplier_create,
    supplier_list,
    supplier_toggle_status,
    supplier_update,
)


urlpatterns = [

    path(
        '',
        supplier_list,
        name='supplier_list'
    ),

    path(
        'add/',
        supplier_create,
        name='supplier_create'
    ),

    path(
        '<int:pk>/edit/',
        supplier_update,
        name='supplier_update'
    ),

    path(
        '<int:pk>/toggle/',
        supplier_toggle_status,
        name='supplier_toggle_status'
    ),
]