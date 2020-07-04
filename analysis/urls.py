from django.urls import path

from . import views

urlpatterns = [
    path('dataclean/', views.DataCleanView.as_view()),
    path('sysanalysis/', views.SysanalysisView.as_view()),
    path('findrootnode/', views.FindrootnodeView.as_view()),
    path('findrootcause/', views.FindrootcauseView.as_view()),
    path('moreanalysis/',views.MoreanalysisView.as_view()),
]
