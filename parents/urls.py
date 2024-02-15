from django.urls import path
from . import views

urlpatterns = [
    path('charges/', views.charges_view, name='charges'),
    path('teachers-list/<int:id>', views.teacher_list_view, name='teacher_list_view'),
]