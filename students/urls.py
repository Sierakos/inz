from django.urls import path
from . import views

urlpatterns = [
    path('grades/<int:id>/', views.student_grades_view, name='student_grades'),
    path('attendance/<int:id>/', views.student_attendance_view, name='student_attendance'),
    path('reports/<int:id>/', views.student_report_view, name='student_report'),
    path('schedule/', views.school_schedule, name='school_schedule'),
]