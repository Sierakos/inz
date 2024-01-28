from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from schedule.models import Lesson
from school.models import Class, Term
from students.models import Student
from grades.models import Assigment, Grade
from subjects.models import Subject

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
def gradebook_view(request, classroom, letter, subject_name):
    classroom_id = Class.objects.get(class_name=classroom, class_letter=letter)

    students = Student.objects.filter(class_id = classroom_id)

    # weź aktualne zajęcie (z url)
    subject = Subject.objects.get(subject_name = subject_name)

    # weź wszystkie kategorie oceny
    assigments = Assigment.objects.all()
    
    grades = Grade.objects.filter(student__in=students, teacher=request.user.teacher, subject=subject)

    dist_lessons = Lesson.objects.filter(class_id=classroom_id).values(
        'class_id',
        'class_id__class_name',
        'class_id__class_letter',
        'class_id__school',
        'teacher_id',
        'subject_id__subject_name').distinct()
    
    lessons = Lesson.objects.all()
    
    print(lessons)

    months_values = {
        'Styczeń': 1,
        'Luty': 2,
        'Marzec': 3,
        'Kwiecień': 4,
        'Maj': 5,
        'Czerwiec': 6
    }

    terms = {
        'Semestr_1': 1,
        'Semestr_2': 2
    }

    context = {
            'students': students,
            'subject': subject,
            'grades': grades,
            'assigments': assigments,
            'months_values': months_values,
            'terms': terms
    }
    


    if request.method == "POST":
        # print(request.POST)
        cleaned_grades = {}

        ### ZMIANA OCENY
        for grade in grades:
            grade_key = 'change_grade_' + str(grade.id)
            if grade_key in request.POST: # dodatkowe zabezpieczenie
                get_grade = Grade.objects.get(id=grade.id)
                get_grade.value = request.POST[grade_key]
                get_grade.save()

        if 'assigment' in request.POST and 'description' in request.POST:
            assigment_name = request.POST['assigment']
            grade_description = request.POST['description']
            assigment_object = Assigment.objects.get(name=assigment_name)
            for student in students:
                grade_key = 'grade_' + str(student.id)
                if grade_key in request.POST: # sprawdź dla kogo ocena została wybrana a dla kogo pominięta
                    grade_value = request.POST[grade_key]
                    cleaned_grades[student.id] = grade_value

                    new_grade = Grade(
                        teacher = request.user.teacher,
                        student = student,
                        subject = subject,
                        assigment = assigment_object,
                        value = grade_value,
                        description = grade_description
                    )

                    new_grade.save()



        return redirect(reverse('gradebook', args=(classroom, letter, subject_name)))

    return render(request, 'teachers/gradebook.html', context=context)

@login_required
def create_assigment(request):
    pass