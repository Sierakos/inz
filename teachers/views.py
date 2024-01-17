from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from schedule.models import Lesson
from school.models import Class
from students.models import Student

from .forms import CreateAssigment

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
def gradebook_view(request, pk, letter, subject):
    lesson = Lesson.objects.get(pk=pk)

    context = {
        'lesson': lesson,
        'pk': pk,
    }

    return render(request, 'teachers/gradebook.html', context=context)

@login_required
def create_assigment(request):
    pass