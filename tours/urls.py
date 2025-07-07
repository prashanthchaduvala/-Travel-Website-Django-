from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('login/', views.email_login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('dashboard/', views.user_dashboard, name='dashboard'),



    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('add/', views.add_tour, name='add_tour'),
    path('tour/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('tour/<int:pk>/pdf/', views.tour_pdf_view, name='tour_pdf'),
    path('add/', views.add_tour, name='add_tour'),
    path('edit/<int:tour_id>/', views.edit_tour, name='edit_tour'),



    path('verify-email/', views.verify_email, name='verify_email'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-reset-otp/', views.verify_reset_otp, name='verify_reset_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
