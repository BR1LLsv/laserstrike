from django.db import models
from django.contrib.auth.models import User

class GameScore(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='game_scores', 
        verbose_name="Гравець"
    )
    score = models.PositiveIntegerField("Рахунок / Очки")
    created_at = models.DateTimeField("Дата гри", auto_now_add=True)

    class Meta:
        verbose_name = "Результат гри"
        verbose_name_plural = "Результати ігор"
        ordering = ['-score']  # Найкращі результати першими

    def __str__(self):
        return f"{self.user.username} — {self.score} очок"