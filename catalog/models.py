from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Arena(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='arenas')
    description = models.TextField()
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    max_players = models.IntegerField(default=10)
    image = models.ImageField(upload_to='arenas/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title