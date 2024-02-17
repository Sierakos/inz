from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from school.forms import ClassForm, ClassroomForm
from school.models import Class, Classroom
from teachers.models import Teacher
from subjects.models import Subject
from accounts.models import CustomUser
from schedule.models import Lesson, LessonInstance

from .forms import SubjectCreateForm, ClassroomCreateForm, ClassCreateForm, ClassUpdateForm, ClassroomUpdateForm, SubjectUpdateForm, LessonCreateForm, LessonInstanceUpdateForm
from accounts.forms import UpdateUserForm

from datetime import datetime

@login_required
def staff_home(request):
    context = {}

    return render(request, 'staff/staff_home.html', context=context)

@login_required
def manage_school(request):

    context = {}

    return render(request, 'staff/manage_school.html', context=context)

@login_required
def users_view(request):

    all_users = CustomUser.objects.all()

    context = {
        'all_users': all_users,
    }

    return render(request, 'staff/users_view.html', context=context)

@login_required
def create_subject_view(request):

    form = SubjectCreateForm()

    if request.method == "POST":
        form = SubjectCreateForm(request.POST)

        form.save()

    context = {
        'form': form,
    }

    return render(request, 'staff/create_subject_view.html', context=context)

@login_required
def update_subject_view(request, id):

    subject_instance = Subject.objects.get(id=id)

    if request.method == "POST":
        form = SubjectUpdateForm(request.POST, instance=subject_instance)
        if form.is_valid():
            form.save()
    else:
        form = SubjectUpdateForm(instance=subject_instance)

    context = {
        'form': form,
    }

    return render(request, 'staff/update_subject_view.html', context=context)

@login_required
def update_user_view(request, id):

    user_instance = CustomUser.objects.get(id=id)

    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=user_instance)
        if form.is_valid():
            form.save()
    else:
        form = UpdateUserForm(instance=user_instance)

    context = {
        'form': form,
    }

    return render(request, 'staff/update_user_view.html', context=context)

@login_required
def subjects_view(request):

    all_subjects = Subject.objects.all()

    context = {
        'all_subjects': all_subjects,
    }

    return render(request, 'staff/subjects_view.html', context=context)

@login_required
def create_classroom_view(request):

    form = ClassroomCreateForm()

    if request.method == "POST":
        form = ClassroomCreateForm(request.POST)

        form.save()

    context = {
        'form': form,
    }

    return render(request, 'staff/create_classroom_view.html', context=context)

@login_required
def update_classroom_view(request, id):

    classroom_instance = Classroom.objects.get(id=id)

    if request.method == "POST":
        form = ClassroomUpdateForm(request.POST,instance=classroom_instance)
        if form.is_valid():
            form.save()
    else:
        form = ClassroomUpdateForm(instance=classroom_instance)

    context = {
        'form': form,
    }

    return render(request, 'staff/update_classroom_view.html', context=context)

@login_required
def classrooms_view(request):

    all_classrooms = Classroom.objects.all()

    context = {
        'all_classrooms': all_classrooms,
    }

    return render(request, 'staff/classrooms_view.html', context=context)

@login_required
def create_class_view(request):

    form = ClassCreateForm()

    if request.method == "POST":
        form = ClassCreateForm(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()

    context = {
        'form': form,
    }

    return render(request, 'staff/create_class_view.html', context=context)

@login_required
def update_class_view(request, id):
    class_instance = Class.objects.get(id=id)

    if request.method == "POST":
        form = ClassUpdateForm(request.POST, instance=class_instance)
        if form.is_valid():
            form.save()
    else:
        form = ClassUpdateForm(instance=class_instance)

    context = {
        'form': form,
    }

    return render(request, 'staff/update_class_view.html', context=context)

@login_required
def class_view(request):

    all_class = Class.objects.all()

    context = {
        'all_class': all_class,
    }

    return render(request, 'staff/class_view.html', context=context)

@login_required
def lessons_view(request):

    all_lessons = Lesson.objects.all()

    context = {
        'all_lessons': all_lessons,
    }

    return render(request, 'staff/lesson_view.html', context=context)

@login_required
def lesson_instances_view(request, id):

    lesson = Lesson.objects.get(id=id)
    lesson_instances = LessonInstance.objects.filter(lesson=lesson)

    context = {
        'lesson': lesson,
        'lesson_instances': lesson_instances
    }

    return render(request, 'staff/lesson_instances_view.html', context=context)

@login_required
def update_lesson_instance_view(request, id):
    lesson_instance = LessonInstance.objects.get(id=id)
    start_time = lesson_instance.get_formated_start_time()
    print(start_time)


    if request.method == "POST":
        date = request.POST['lesson_day']
        formated_date = datetime.strptime(date, '%d.%m.%Y').date()
        form = LessonInstanceUpdateForm(request.POST)
        lesson_instance.lesson_day = formated_date
        start_time, end_time = request.POST['lesson_hours'].split('-')
        lesson_instance.lesson_start_time = start_time
        lesson_instance.lesson_end_time = end_time
        lesson_instance.save()

    else:
        form = LessonInstanceUpdateForm(instance=lesson_instance)

    context = {
        'form': form,
        'start_time': start_time
    }

    return render(request, 'staff/update_lesson_instances_view.html', context=context)


@login_required
def create_lesson_view(request):
    if request.method == 'POST':
        form = LessonCreateForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = LessonCreateForm()
    return render(request, 'staff/create_lesson_view.html', {'form': form})
