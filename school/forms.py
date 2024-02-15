from django import forms 

from django import forms
from .models import Class, Classroom

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['class_name', 'class_letter', 'school', 'counselor']

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['room_number']