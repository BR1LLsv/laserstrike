from django.contrib import admin
from .models import Booking, Payment

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'arena', 'booking_date', 'start_time', 'end_time', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'booking_date', 'arena')
    search_fields = ('user__username', 'arena__title', 'id')
    list_editable = ('status',)  # Адмін може швидко міняти статус ("Очікує оплати" -> "Оплачено")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'amount', 'status', 'transaction_id', 'paid_at')
    list_filter = ('status',)
    search_fields = ('transaction_id', 'booking__id')