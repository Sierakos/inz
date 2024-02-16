from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from school.forms import ClassForm, ClassroomForm
from school.models import Class, Classroom
from teachers.models import Teacher
from subjects.models import Subject
from accounts.models import CustomUser

from .forms import SubjectCreateForm, ClassroomCreateForm, ClassCreateForm, ClassUpdateForm, ClassroomUpdateForm, SubjectUpdateForm

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
