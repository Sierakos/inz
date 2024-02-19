from django import forms

from grades.models import Assigment, Grade, StudentReport
from schedule.models import Lesson
from school.models import Class, Classroom
from subjects.models import Subject
from teachers.models import Teacher
from schedule.models import Lesson, LessonInstance

from datetime import datetime

class LessonCreateForm(forms.ModelForm):
    sem_1 = forms.BooleanField(label='Semester 1', required=False, widget=forms.RadioSelect(choices=((True, 'Tak'), (False, 'Nie'))))
    sem_2 = forms.BooleanField(label='Semester 2', required=False, widget=forms.RadioSelect(choices=((True, 'Tak'), (False, 'Nie'))))
    class Meta:
        model = Lesson
        fields = ['class_id', 'subject_id', 'teacher_id', 'room_id', 'term_id', 'day', 'lesson_hours', 'sem_1', 'sem_2']

        labels = {
            'class_id': 'Klasa',
            'subject_id': 'Przedmiot',
            'teacher_id': 'Prowadzący',
            'room_id': 'Sala',
            'term_id': 'Wybór semestru',
            'day': 'Dzień',
            'lesson_hours': 'Godziny odbywania sięzajęć',
            'sem_1': 'Czy dane zajęcia będą odbywane w semestrze pierwszym?',
            'sem_2': 'Czy dane zajęcia będą odbywane w semestrze drugim?',
        }

        widgets = {}
        for field in fields:
            widgets[field] = forms.Select(attrs={'class': 'form-control'})

class ClassCreateForm(forms.ModelForm):
    # counselor = forms.ModelChoiceField(queryset=Teacher.objects.exclude(class__isnull=False))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        existing_counselors_ids = Class.objects.values_list('counselor', flat=True)
        self.fields['counselor'].queryset = Teacher.objects.exclude(class__isnull=False) # class__isnull czyli czy nie ma przypisanej żadnej klasy
        # counselor = forms.ModelChoiceField(queryset=qs)

    class Meta:
        model = Class
        fields = ['class_name', 'class_letter', 'school', 'counselor']

        labels = {
            'class_name': 'Stopień klasy',
            'class_letter': 'Nazwa klasy',
            'school': 'Szkoła',
            'counselor': 'Wychowawca',
        }
        widgets = {
            'class_name': forms.Select(attrs={'class': 'form-control'}),
            'class_letter': forms.Select(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'counselor': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        class_name = cleaned_data.get('class_name')
        class_letter = cleaned_data.get('class_letter')

        # Sprawdzenie, czy klasa o tej samej klasie i literze już istnieje
        existing_classes = Class.objects.filter(class_name=class_name, class_letter=class_letter)
        if self.instance and self.instance.pk:
            existing_classes = existing_classes.exclude(pk=self.instance.pk)  # Wykluczenie bieżącej instancji
        if existing_classes.exists():
            raise forms.ValidationError("Klasa o tym samym stopniu i literze już istnieje.")

        return cleaned_data
    

class LessonInstanceUpdateForm(forms.ModelForm):
    class Meta:
        model = LessonInstance
        fields = ['lesson_day']

        labels = {
            'lesson_day': 'Dzień odbywania się zajęć'
        }

        widgets = {
            'lesson_day': forms.TextInput(attrs={'class': 'form-control', 'id': 'lesson_day'}),
        }

    def __init__(self, *args, **kwargs):
        super(LessonInstanceUpdateForm, self).__init__(*args, **kwargs)
        # Nadpisanie wartości daty w formularzu
        if 'lesson_day' in self.initial:
            self.initial['lesson_day'] = self.initial['lesson_day'].strftime('%d.%m.%Y')
    
class ClassUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        existing_counselors_ids = Class.objects.values_list('counselor', flat=True)
        self.fields['counselor'].queryset = Teacher.objects.exclude(class__isnull=False) # class__isnull czyli czy nie ma przypisanej żadnej klasy
        print(existing_counselors_ids)

    class Meta:
        model = Class
        fields = ['class_name', 'class_letter', 'school', 'counselor']

        labels = {
            'class_name': 'Stopień klasy',
            'class_letter': 'Nazwa klasy',
            'school': 'Szkoła',
            'counselor': 'Wychowawca',
        }
        widgets = {
            'class_name': forms.Select(attrs={'class': 'form-control'}),
            'class_letter': forms.Select(attrs={'class': 'form-control'}),
            'school': forms.Select(attrs={'class': 'form-control'}),
            'counselor': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        class_name = cleaned_data.get('class_name')
        class_letter = cleaned_data.get('class_letter')

        # Sprawdzenie, czy klasa o tej samej klasie i literze już istnieje
        existing_classes = Class.objects.filter(class_name=class_name, class_letter=class_letter)
        if self.instance and self.instance.pk:
            existing_classes = existing_classes.exclude(pk=self.instance.pk)  # Wykluczenie bieżącej instancji
        if existing_classes.exists():
            raise forms.ValidationError("Klasa o tym samym stopniu i literze już istnieje.")

        return class_name
    
    def clean_counselor(self):
        cleaned_data = super().clean()
        counselor_id = cleaned_data.get('counselor')

        if counselor_id:
            # Sprawdź, czy nauczyciel jest już przypisany do innej klasy
            existing_class = Class.objects.filter(counselor_id=counselor_id)
            if self.instance and self.instance.pk:
                existing_class = existing_class.exclude(pk=self.instance.pk)  # Wykluczenie bieżącej instancji
            if existing_class.exists():
                raise forms.ValidationError("Ten nauczyciel jest już przypisany do innej klasy.")

        return counselor_id

class SubjectCreateForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name']

        labels = {
            'subject_name': 'Nazwa przedmiotu'
        }
        widgets = {
                'subject_name': forms.TextInput(attrs={'class': 'form-control'})
            }
        
class SubjectUpdateForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['subject_name']

        labels = {
            'subject_name': 'Nazwa przedmiotu'
        }
        widgets = {
                'subject_name': forms.TextInput(attrs={'class': 'form-control'})
            }


class ClassroomCreateForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['room_number']
        labels = {
            'room_number': 'Numer sali'
        }
        widgets = {
                'room_number': forms.TextInput(attrs={'class': 'form-control'})
            }
        
class ClassroomUpdateForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['room_number']
        labels = {
            'room_number': 'Numer sali'
        }
        widgets = {
                'room_number': forms.TextInput(attrs={'class': 'form-control'})
            }

        


