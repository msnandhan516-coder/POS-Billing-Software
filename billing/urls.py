from django.urls import path

from .api_views import checkout
from .views import invoice, pos, sales_history


urlpatterns = [

    path(
        '',
        pos,
        name='pos'
    ),

    path(
        'checkout/',
        checkout,
        name='checkout'
    ),

    path(
        'invoice/<str:invoice_number>/',
        invoice,
        name='invoice'
    ),

    path(
    'sales/',
    sales_history,
    name='sales_history'
),

]