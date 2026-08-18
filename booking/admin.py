from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'arena', 'booking_date', 'start_time', 'end_time', 'status', 'total_price')
    list_filter = ('status', 'booking_date', 'arena')
    search_fields = ('user__username', 'arena__title')