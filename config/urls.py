from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

from .views import admin_dashboard


urlpatterns = [

    path(
        'django-admin/',
        admin.site.urls
    ),

    path(
        '',
        include('accounts.urls')
    ),

    path(
        'admin-dashboard/',
        admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'billing/',
        include('billing.urls')
    ),

    path(
        'products/',
        include('products.urls')
    ),

    path(
        'suppliers/',
        include('suppliers.urls')
    ),

    path(
        'media/<path:path>',
        serve,
        {
            'document_root': settings.MEDIA_ROOT,
        },
    ),
]