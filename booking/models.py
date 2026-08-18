from django.db import models
from django.contrib.auth.models import User
from catalog.models import Arena

class Booking(models.Model):
    STATUS_CHOICES = [
        ('new', 'Нове'),
        ('paid', 'Оплачено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    arena = models.ForeignKey(Arena, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    players_count = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.id} - {self.arena.title} ({self.user.username})"