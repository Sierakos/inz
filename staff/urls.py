from django.urls import path
from . import views

urlpatterns = [
    path('/', views.staff_home, name='staff_home'),
    path('manage-school/', views.manage_school, name='manage_school'),
    path('users/', views.users_view, name='users'),
    path('create-subject/', views.create_subject_view, name='create_subjects'),
    path('subjects/', views.subjects_view, name='subjects'),
    path('create-classroom/', views.create_classroom_view, name='create_classroom'),
    path('classrooms/', views.classrooms_view, name='classrooms'),
    path('create-class/', views.create_class_view, name='create_class'),
    path('class/', views.class_view, name='class'),
    # updates
    path('update-class/<int:id>/', views.update_class_view, name='update_class'),
    path('update-classroom/<int:id>/', views.update_classroom_view, name='update_classroom'),
    path('update-subject/<int:id>/', views.update_subject_view, name='update_subject'),
]