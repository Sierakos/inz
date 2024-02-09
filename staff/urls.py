from django.urls import path
from . import views

urlpatterns = [
    path('/', views.staff_home, name='staff_home'),
    path('manage-school/', views.manage_school, name='manage_school'),
]