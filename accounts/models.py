from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile', 
        verbose_name="Користувач"
    )
    avatar = models.ImageField(
        "Аватар", 
        upload_to='avatars/', 
        default='avatars/default.png', 
        blank=True, 
        null=True
    )
    phone = models.CharField("Номер телефону", max_length=20, blank=True, null=True)
    bio = models.TextField("Про себе / Позивний", blank=True, null=True)
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)

    class Meta:
        verbose_name = "Профіль користувача"
        verbose_name_plural = "Профілі користувачів"

    def __str__(self):
        return f"Профіль гравця: {self.user.username}"