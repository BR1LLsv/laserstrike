from django.contrib import admin
from .models import Category, Arena

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Arena)
class ArenaAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price_per_hour', 'max_players', 'is_available')
    list_filter = ('category', 'is_available')
    search_fields = ('title', 'description')