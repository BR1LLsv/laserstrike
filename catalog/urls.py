from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('arena/<int:pk>/', views.arena_detail, name='arena_detail'),  # <--- Додано
    path('shooting-range/', views.shooting_range_view, name='shooting_range'),
]