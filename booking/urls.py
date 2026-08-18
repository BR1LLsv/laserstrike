from django.urls import path
from . import views

urlpatterns = [
    path('pay/<int:booking_id>/', views.payment_view, name='pay_booking'),
    path('ticket/<int:booking_id>/', views.ticket_view, name='ticket_view'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]