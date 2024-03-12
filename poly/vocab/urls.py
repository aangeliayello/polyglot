from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('word_with_context/', views.word_with_context_view, name='word_with_context_form'),
    path("save_translation/", views.save_translation_result, name="save_translation_result"),
    path('update-translation/<int:translation_id>/', views.update_translation, name='update_translation')
]