from django.urls import path
from . import views

urlpatterns = [
    path('/', views.staff_home, name='staff_home'),
    path('manage-school/', views.manage_school, name='manage_school'),
    path('users/', views.users_view, name='users'),
    path('subjects/', views.subjects_view, name='subjects'),
    path('classrooms/', views.classrooms_view, name='classrooms'), 
    path('class/', views.class_view, name='class'),
    path('lessons/', views.lessons_view, name='lessons'),
    path('lessons-instances/<int:id>', views.lesson_instances_view, name='lessons_instances'),
    # creates
    path('create-subject/', views.create_subject_view, name='create_subjects'),
    path('create-classroom/', views.create_classroom_view, name='create_classroom'),
    path('create-class/', views.create_class_view, name='create_class'),
    path('create-lesson/', views.create_lesson_view, name='create_lesson'),
    # updates
    path('update-class/<int:id>/', views.update_class_view, name='update_class'),
    path('update-classroom/<int:id>/', views.update_classroom_view, name='update_classroom'),
    path('update-subject/<int:id>/', views.update_subject_view, name='update_subject'),
    path('update-user/<int:id>/', views.update_user_view, name='update_user'),
    path('update-lesson-instance/<int:id>/', views.update_lesson_instance_view, name='update_lesson_instance'),
]