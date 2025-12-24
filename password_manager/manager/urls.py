# manager/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add/', views.add_password_view, name='add_password'),
    path('', views.home_view, name='hyome'),
    path('get-password/<int:entry_id>/', views.get_password_view, name='get_password'),
    path('edit/<int:entry_id>/', views.edit_password_view, name='edit_password'),
    path('delete/<int:entry_id>/', views.delete_password_view, name='delete_password'),
]