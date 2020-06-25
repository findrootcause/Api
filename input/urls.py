from django.urls import path

from . import views

urlpatterns = [
    path('', views.FileRecordsView.as_view()),
]
