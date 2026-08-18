from django.contrib import admin
from .models import GameScore

@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)