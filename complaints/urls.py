from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('submit/', views.submit_complaint, name='submit_complaint'),
    path('complaints/', views.complaint_list, name='complaint_list'),
    path('profile/', views.profile, name='profile'),
    path('complaint/<int:pk>/', views.complaint_detail, name='complaint_detail'),
]
