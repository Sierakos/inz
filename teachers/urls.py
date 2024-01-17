from django.urls import path
from . import views

urlpatterns = [
    path('teacher_subjects/', views.teacher_subjects_view, name='teacher_subjects'),
    path('gradebook/<int:pk>/<str:letter>/<str:subject>', views.gradebook_view, name='gradebook'),
    path('create_assigment/', views.gradebook_view, name='gradebook')
]