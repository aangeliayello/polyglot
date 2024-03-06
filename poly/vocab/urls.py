from django.urls import path

from .views import WordWithContextView
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('word_with_context/', views.word_with_context_view, name='word_with_context'),
    
]