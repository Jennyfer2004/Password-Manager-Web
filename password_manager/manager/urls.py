# manager/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add/', views.add_password_view, name='add_password'),
    path('logout/', views.custom_logout, name='logout'),
    path('', views.home_view, name='hyome'),
    path('get-password/<int:entry_id>/', views.get_password_view, name='get_password'),
    path('edit/<int:entry_id>/', views.edit_password_view, name='edit_password'),
    path('delete/<int:entry_id>/', views.delete_password_view, name='delete_password'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('registro-exitoso/', views.email_sent_view, name='email_sent'),
    path('login/password-reset/', views.password_reset_request_view, name='password_reset'),
    path('login/password-reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('login/reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('login/password-reset-complete/', views.password_reset_complete_view, name='password_reset_complete'),
]