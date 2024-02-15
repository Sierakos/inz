from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Parent
from students.models import Student
from teachers.models import Teacher
from schedule.models import Lesson

@login_required()
def charges_view(request):

    actual_account = request.user

    parent = Parent.objects.get(parent=actual_account)
    
    students = Student.objects.filter(parent_id=parent)

    context={
        'students': students,
    }

    return render(request, 'parents/charges_view.html', context=context)

@login_required()
def teacher_list_view(request, id):
    
    student = Student.objects.get(id=id)
    student_class = student.class_id

    teacher_list = []
    # dostaję z tego tylko ID nauczycieli a nie ich obiekty
    # <TODO: czy można lepiej>
    teachers = Lesson.objects.filter(class_id=student_class).values_list('teacher_id', flat=True).distinct()
    

    teachers_subjects = {}
    

    for teacher in teachers:
        teacher_object = Teacher.objects.get(id=teacher) # przekształcanie id nauczyciela w obiekt nauczyciela
        lessons = Lesson.objects.filter(class_id=student_class, teacher_id__id=teacher)
        
        # zwróci liste przedmiotów które uczy w danej klasie 
        # dany nauczyciel
        teacher_subject = []
        for lesson in lessons:
            if lesson.subject_id.subject_name not in teacher_subject:
                teacher_subject.append(lesson.subject_id.subject_name)

        teachers_subjects[teacher_object] = teacher_subject

    context={
        'student': student,
        'teachers_subjects': teachers_subjects
    }

    return render(request, 'parents/teachers_list_view.html', context=context)