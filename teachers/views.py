from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse

from django.core.mail import send_mail
from django.core.mail import EmailMessage


from schedule.models import Lesson, LessonInstance
from school.models import Class, Term
from students.models import Student, StudentAttendance
from grades.models import Assigment, Grade, StudentReport
from subjects.models import Subject
from parents.models import Parent
from .models import Teacher

from .forms import CreateAssigment, ContactForm, StudentReportForm

from datetime import datetime

from .utils import *

import json

from reportlab.pdfgen import canvas


@login_required
def home_redirect(request):
    return redirect(reverse('teacher_subjects'))

@login_required
def teacher_subjects_view(request):
    user = request.user
    teacher = user.teacher
    lessons = Lesson.objects.filter(teacher_id = teacher.id)
    students = Student.objects.all()

    dist_lessons = Lesson.objects.filter(teacher_id=teacher).values(
        'class_id',
        'class_id__class_name',
        'class_id__class_letter',
        'class_id__school',
        'teacher_id',
        'subject_id__subject_name',
        'subject_id__id',
        'class_id__id').distinct()
    
    # grades = Grade.objects.all()

    ### potrzebne do wykresów klas
    data = []
    for lesson in dist_lessons:

        ### weź uczniów, którzy uczęszczają na dane zajęcia
        actual_students = Student.objects.filter(class_id = int(lesson['class_id__id']))

        ### weź średnie oceny dla każdego z uczniów uczęszczający
        ### na dane zajęcia

        students_avarage = {}
        for student in actual_students:
            students_avarage[str(student.student.first_name + " " + student.student.last_name)] = Grade.get_avarage_grade_without_term(student=student, subject=int(lesson['subject_id__id']))
        

        data.append({
            f"{lesson['class_id']}_{lesson['class_id__class_letter']}_{lesson['subject_id__id']}": students_avarage,
        })

    jsonData = json.dumps(data)

    # do planu zajęć
    hours_choices = Lesson.LESSON_HOURS_CHOICES
    hours = []
    for hour_choice in hours_choices:
        hours.append(hour_choice[0])

    days_choice = Lesson.DAY_CHOICES
    days = []
    for day_choice in days_choice:
        days.append(day_choice[0])

    hours_lesson = {}
    for lesson in lessons:
        hours_lesson[lesson.lesson_hours] = [Lesson.objects.filter(teacher_id = teacher.id, lesson_hours=lesson.lesson_hours)]

    print(hours_lesson)
    
    form = CreateAssigment(teacher = request.user.teacher)

    context = {
        'dist_lessons': dist_lessons,
        'form': form,
        'students': students,
        'jsonData': jsonData,
        'hours': hours,
        'lessons': lessons,
        'hours_lesson': hours_lesson,
        'days': days
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
    
    grades = Grade.objects.filter(student__in=students, teacher=request.user.teacher, subject=subject, assigment__midterm_grade=False, assigment__final_grade=False)

    actual_lesson = Lesson.objects.filter(class_id = classroom_id, subject_id=subject).values(
        'class_id',
        'class_id__class_name',
        'class_id__class_letter',
        'class_id__school',
        'teacher_id',
        'subject_id__subject_name',
        'subject_id__id',
        'term_id').distinct()

    ### wez semestr z danego przedmiotu
    ### potrzebne do ustalenia dziennika od kiedy
    ### do kiedy jest pierwszy oraz drugi semestr
    term = Term.objects.get(id=actual_lesson[0]['term_id']) # <TODO> czy jest inna opcja poza [0]

    # stara wersja
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

    # przypisanie ocen do danego semestru
    # <TODO> dowiedzieć się czy nie lepiej
    # przypisać z poziomu modelu
    grades_with_terms = {}
    for grade in grades:
        convert_grade_date = grade.created_at.date()
        if between(convert_grade_date, term.term_start_sem_1, term.term_end_sem_1) == True:
            grades_with_terms[grade] = terms['Semestr_1']
        elif between(convert_grade_date, term.term_start_sem_2, term.term_end_sem_2) == True:
            grades_with_terms[grade] = terms['Semestr_2']
        else:
            pass

    # średnie ważone dla każdego z ucznia
    # w danym semestrze
    avarages_with_terms = {}
    for student in students:

        avarage = Grade.get_avarage_grade(student, subject, term)
        avarages_with_terms[student] = avarage

    print(avarages_with_terms)

    # formularz uwag
    report_form = StudentReportForm(request.POST, students=students)

    context = {
            'students': students,
            'subject': subject,
            'grades': grades,
            'assigments': assigments,
            'months_values': months_values,
            'terms': terms,
            'term': term,
            'grades_with_terms': grades_with_terms,
            'avarages_with_terms': avarages_with_terms,
            'report_form': report_form,
            'class_name': classroom,
            'class_letter': letter,
            'subject': subject
    }

    if request.method == "POST":
        # print(request.POST)
        cleaned_grades = {}
        print(request.POST)

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

                    # sprawdź czy nie ma już oceny końcowej lub średniej dla danego ucznia w przypadku ich wpisywania
                    if assigment_object.midterm_grade == True:
                        is_midterm_grade = Grade.objects.filter(
                            teacher = request.user.teacher,
                            student = student,
                            subject = subject,
                            assigment = assigment_object,
                            assigment__midterm_grade=True).exists()
                        if is_midterm_grade:
                            midterm_grade = Grade.objects.filter(
                                teacher = request.user.teacher,
                                student = student,
                                subject = subject,
                                assigment = assigment_object,
                                assigment__midterm_grade=True)
                            
                            midterm_grade.update(value=grade_value)

                        else:
                            new_grade = Grade(
                            teacher = request.user.teacher,
                            student = student,
                            subject = subject,
                            assigment = assigment_object,
                            value = grade_value,
                            description = grade_description
                            )

                            new_grade.save()

                    elif assigment_object.final_grade == True:
                        is_final_grade = Grade.objects.filter(
                            teacher = request.user.teacher,
                            student = student,
                            subject = subject,
                            assigment = assigment_object,
                            assigment__final_grade=True
                                                ).exists()
                        if is_final_grade:
                            final_grade = Grade.objects.filter(
                                teacher = request.user.teacher,
                                student = student,
                                subject = subject,
                                assigment = assigment_object,
                                assigment__final_grade=True)
                            
                            final_grade.update(value=grade_value)
                        else:
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
def add_report(request, class_name, class_letter, subject):
    classroom_id = Class.objects.get(class_name=class_name, class_letter=class_letter)

    students = Student.objects.filter(class_id = classroom_id)

    subject = Subject.objects.get(subject_name=subject)

    if request.method == 'POST':
        report_form = StudentReportForm(request.POST, students=students)
        if report_form.is_valid():
            student_report = report_form.save(commit=False)
            student_report.teacher = request.user.teacher
            student_report.subject = subject
            student_report.save()

        return redirect(reverse('gradebook', args=(class_name, class_letter, subject)))


@login_required
def contact_parent_view(request, student):
    form = ContactForm()

    current_student = Student.objects.get(pk=student)
    current_parent = current_student.parent_id

    print(current_parent.parent.email)

    receiver_email = current_parent.parent.email
    sender_email = request.user.email

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            body = form.cleaned_data['body']

            body += f"\n\nWysłano przez: {request.user.user_type} {request.user.first_name} { request.user.last_name }"

            # send_mail(
            #     title,
            #     body,
            #     'settings.EMAIL_HOST_USER',
            #     [receiver_email],
            #     fail_silently=False
            # )

            email = EmailMessage(
                title,
                body,
                "settings.EMAIL_HOST_USER",
                [receiver_email],
                reply_to=[sender_email]
            )

            email.send()



        return redirect(reverse('contact_parent', args=(student,)))

    context = {
        'form': form,
        'current_parent': current_parent
    }

    return render(request, 'teachers/contact_parent.html', context=context)

@login_required
def create_assigment(request):
    pass

def lessons_view(request, classroom, letter, subject_name):

    classroom_id = Class.objects.get(class_name=classroom, class_letter=letter)

    subject = Subject.objects.get(subject_name = subject_name)

    actual_lesson = Lesson.objects.filter(class_id = classroom_id, subject_id=subject)

    lessons = LessonInstance.objects.filter(lesson__in=actual_lesson.all())
    
    context = {
        'lessons': lessons
    }

    return render(request, 'teachers/lessons_view.html', context=context)

@login_required
def check_attendance_view(request, id):

    actual_lesson_instance = LessonInstance.objects.get(id=id)

    related_lesson = actual_lesson_instance.lesson

    students = Student.objects.filter(class_id=related_lesson.class_id)

    students_atts = StudentAttendance.objects.filter(lesson=actual_lesson_instance)
    print(students_atts)

    context = {
        'lesson': actual_lesson_instance,
        'students_atts': students_atts,
        'students': students
    }

    cleaned_attendances = {}
    for student in students:
        attendance_key = 'attendance_' + str(student.id)
        if attendance_key in request.POST:
            print("aaa")
            attendance_value = request.POST[attendance_key]
            cleaned_attendances[student.id] = attendance_value

            if attendance_value == "OB":
                student_attendance = StudentAttendance.objects.filter(
                    student=student,
                    lesson=actual_lesson_instance
                ).update(
                    is_present = True,
                    is_absent = False,
                    is_late = False
                )
            elif attendance_value == "NB":
                student_attendance = StudentAttendance.objects.filter(
                    student=student,
                    lesson=actual_lesson_instance
                ).update(
                    is_present = False,
                    is_absent = True,
                    is_late = False
                )
            elif attendance_value == "SP":
                student_attendance = StudentAttendance.objects.filter(
                    student=student,
                    lesson=actual_lesson_instance
                ).update(
                    is_present = False,
                    is_absent = False,
                    is_late = True
                )

    print(cleaned_attendances)

    return render(request, 'teachers/check_attendance_view.html', context=context)

@login_required
def start_lesson(request, id):
    actual_lesson_instance = LessonInstance.objects.get(id=id)

    related_lesson = actual_lesson_instance.lesson

    students = Student.objects.filter(class_id=related_lesson.class_id)

    # for redirect
    subject_name = related_lesson.subject_id.subject_name
    class_name = related_lesson.class_id.class_name
    class_letter = related_lesson.class_id.class_letter
    
    if actual_lesson_instance.is_started == False:
        # Only one of Lesson instance can be started at once
        lessons_instances = LessonInstance.objects.filter(lesson=related_lesson)
        for lesson_instance in lessons_instances:
            if lesson_instance.is_started:
                return redirect(reverse('lessons_view', args=(class_name, class_letter, subject_name)))

        actual_lesson_instance.is_started = True
        actual_lesson_instance.save()

        for student in students:
            if not StudentAttendance.objects.filter(student=student, lesson=actual_lesson_instance).exists():
                StudentAttendance.objects.create(student=student, lesson=actual_lesson_instance)

    # For undo start purpose
    elif actual_lesson_instance.is_started == True:

        actual_lesson_instance.is_started = False
        actual_lesson_instance.save()

        for student in students:
            if StudentAttendance.objects.filter(student=student, lesson=actual_lesson_instance).exists():
                StudentAttendance.objects.filter(student=student, lesson=actual_lesson_instance).delete()


    return redirect(reverse('lessons_view', args=(class_name, class_letter, subject_name)))

@login_required
def end_lesson(request, id):
    actual_lesson_instance = LessonInstance.objects.get(id=id)

    related_lesson = actual_lesson_instance.lesson

    students = Student.objects.filter(class_id=related_lesson.class_id)

    # for redirect
    subject_name = related_lesson.subject_id.subject_name
    class_name = related_lesson.class_id.class_name
    class_letter = related_lesson.class_id.class_letter

    actual_lesson_instance.is_started = False
    actual_lesson_instance.is_finished = True
    actual_lesson_instance.save()

    return redirect(reverse('lessons_view', args=(class_name, class_letter, subject_name)))

@login_required
def my_class_view(request):
    
    actual_teacher = request.user.teacher
    teacher_class = Class.objects.get(counselor=actual_teacher)

    students = Student.objects.filter(class_id=teacher_class)

    last_reports = StudentReport.objects.filter(student__in=students.all()).order_by('-created_at')[:5]
    last_absents = StudentAttendance.objects.filter(student__in=students.all(), is_absent=True).order_by('-created_at')[:5]
    
    context = {
        'class': teacher_class,
        'students': students,
        'last_reports': last_reports,
        'last_absents': last_absents
    }

    return render(request, 'teachers/my_class_view.html', context=context)

@login_required
def generate_student_raport(request, id):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="student_report.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, "Raport Ucznia")  # Tytuł raportu
    # Tutaj dodaj więcej zawartości raportu w odpowiednich miejscach na stronie
    p.showPage()
    p.save()

    return response

@login_required
def messages_view(request):

    students = Student.objects.all()
    teachers = Teacher.objects.exclude(teacher__id=request.user.id)

    context = {
        'students': students,
        'teachers': teachers
    }

    return render(request, 'teachers/messages_view.html', context=context)