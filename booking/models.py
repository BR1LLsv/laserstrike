from django.db import models
from django.contrib.auth.models import User
from catalog.models import Arena

class Booking(models.Model):
    STATUS_CHOICES = [
        ('new', 'Очікує оплати'),
        ('paid', 'Оплачено'),
        ('cancelled', 'Скасовано'),
        ('completed', 'Завершено'),
    ]

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='bookings', 
        verbose_name="Користувач"
    )
    arena = models.ForeignKey(
        Arena, 
        on_delete=models.CASCADE, 
        related_name='bookings', 
        verbose_name="Арена"
    )
    booking_date = models.DateField("Дата гри")
    start_time = models.TimeField("Час початку")
    end_time = models.TimeField("Час завершення")
    players_count = models.PositiveIntegerField("Кількість гравців", default=1)
    total_price = models.DecimalField("Загальна вартість (грн)", max_digits=10, decimal_places=2)
    status = models.CharField("Статус", max_length=20, choices=STATUS_CHOICES, default='new')
    comment = models.TextField("Коментар до замовлення", blank=True, null=True)
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)

    class Meta:
        verbose_name = "Бронювання"
        verbose_name_plural = "Бронювання"

    def __str__(self):
        return f"Бронювання №{self.id} — {self.arena.title} ({self.user.username})"


class Payment(models.Model):
    booking = models.OneToOneField(
        Booking, 
        on_delete=models.CASCADE, 
        related_name='payment', 
        verbose_name="Бронювання"
    )
    amount = models.DecimalField("Сума оплати", max_digits=10, decimal_places=2)
    status = models.CharField("Статус", max_length=20, default='success')
    transaction_id = models.CharField("ID транзакції", max_length=100, blank=True)
    paid_at = models.DateTimeField("Дата й час оплати", auto_now_add=True)

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплати"

    def __str__(self):
        return f"Оплата №{self.id} для замовлення №{self.booking.id}"