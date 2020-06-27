from django.urls import path

from . import views

urlpatterns = [
    path('dataclean/', views.DataCleanView.as_view()),
]
