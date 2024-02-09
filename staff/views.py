from django.shortcuts import render

from django.contrib.auth.decorators import login_required

@login_required
def staff_home(request):

    context = {}

    return render(request, 'staff/staff_home.html', context=context)

@login_required
def manage_school(request):
    context = {}

    return render(request, 'staff/manage_school.html', context=context)