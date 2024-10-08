from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('download-sample/', views.download_sample, name='download_sample'),
    path('master/', views.master, name='master'),
    path('output/', views.output, name='output'),
    path('master/delete/<int:pk>/', views.delete_master, name='delete_master'),
    path('master/edit/<int:pk>/', views.edit_master, name='edit_master'),
    path('confirm_master/', views.confirm_master, name='confirm_master'),
]
