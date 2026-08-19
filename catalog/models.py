from django.db import models
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField("Назва категорії", max_length=100)
    slug = models.SlugField("URL-слаг", unique=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return self.name


class Arena(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='arenas', 
        verbose_name="Категорія"
    )
    title = models.CharField("Назва арени/майданчика", max_length=200)
    description = models.TextField("Опис")
    price_per_hour = models.DecimalField("Ціна за годину (грн)", max_digits=8, decimal_places=2)
    photo = CloudinaryField('image')
    max_players = models.PositiveIntegerField("Макс. кількість гравців", default=10)
    is_available = models.BooleanField("Доступно для бронювання", default=True)
    created_at = models.DateTimeField("Дата створення", auto_now_add=True)

    class Meta:
        verbose_name = "Арена"
        verbose_name_plural = "Арени"

    def __str__(self):
        return self.title