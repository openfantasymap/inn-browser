from django.urls import path
from . import views

urlpatterns = [
    # Game API endpoints will be added here
    path('health/', views.health_check, name='health'),
]
