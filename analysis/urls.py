from django.urls import path

from . import views

urlpatterns = [
    path('DataCleanView/', views.DataCleanView.as_view()),
    path('Findrootcause/', views.Findrootcause.as_view()),
    path('Findrootnode/', views.Findrootnode.as_view()),
    path('Sysanalysis/', views.Sysanalysis.as_view()),

]
