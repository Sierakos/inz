from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from schedule.models import Lesson
from school.models import Class
from students.models import Student
from grades.models import Assigment, Grade
from subjects.models import Subject

from .forms import CreateAssigment, GradeForm

@login_required
def teacher_subjects_view(request):
    user = request.user
    teacher = user.teacher
    # lessons = Lesson.objects.filter(teacher_id = teacher.id)
    students = Student.objects.all()

    dist_lessons = Lesson.objects.filter(teacher_id=teacher).values(
        'class_id',
        'class_id__class_name',
        'class_id__class_letter',
        'class_id__school',
        'teacher_id',
        'subject_id__subject_name').distinct()
    
    form = CreateAssigment(teacher = request.user.teacher)

    context = {
        'lessons': dist_lessons,
        'form': form,
        'students': students
    }

    return render(request, 'teachers/teacher_subjects.html', context=context)

@login_required
def gradebook_view(request, classroom, letter, subject):
    classroom_id = Class.objects.get(class_name=classroom, class_letter=letter)

    students = Student.objects.filter(class_id = classroom_id)

    # weź aktualne zajęcie (z url)
    subject_id = Subject.objects.get(subject_name = subject)

    # Weź powód oceny (np test, praca domowa)
    # za pomocą id klasy oraz aktualnychj zajęć (z url)
    assigments = Assigment.objects.filter(class_id = classroom_id, subject_id = subject_id)

    grades = Grade.objects.filter(assigment__in = assigments)

    print(grades)

    print(assigments)

    assigment_ids = [assigment.id for assigment in assigments]

    form = GradeForm(initial={'assigment_ids': assigment_ids})

    context = {
        'students': students,
        'subject': subject,
        'assigments': assigments,
        'grades': grades,
        'form': form,
    }

    return render(request, 'teachers/gradebook.html', context=context)

@login_required
def create_assigment(request):
    pass