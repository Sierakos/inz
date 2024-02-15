from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required

from school.forms import ClassForm, ClassroomForm
from school.models import Class, Classroom
from teachers.models import Teacher

@login_required
def staff_home(request):
    context = {}

    return render(request, 'staff/staff_home.html', context=context)

@login_required
def manage_school(request):

    context = {}

    return render(request, 'staff/manage_school.html', context=context)

@login_required
def add_class(request):
    if request.method == 'POST':
        form = ClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Zastąp 'success_url' adresem URL do przekierowania po zapisaniu
    else:
        form = ClassForm()
    return render(request, 'add_class.html', {'form': form})

@login_required
def edit_class(request, class_id):
    instance = Class.objects.get(id=class_id)
    if request.method == 'POST':
        form = ClassForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Zastąp 'success_url' adresem URL do przekierowania po zapisaniu
    else:
        form = ClassForm(instance=instance)
    return render(request, 'edit_class.html', {'form': form})

@login_required
def add_classroom(request):
    if request.method == 'POST':
        form = ClassroomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Zastąp 'success_url' adresem URL do przekierowania po zapisaniu
    else:
        form = ClassroomForm()
    return render(request, 'add_classroom.html', {'form': form})

@login_required
def edit_classroom(request, classroom_id):
    instance = Classroom.objects.get(id=classroom_id)
    if request.method == 'POST':
        form = ClassroomForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # Zastąp 'success_url' adresem URL do przekierowania po zapisaniu
    else:
        form = ClassroomForm(instance=instance)
    return render(request, 'edit_classroom.html', {'form': form})