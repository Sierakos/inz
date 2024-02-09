from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect

from grades.models import Grade, StudentReport
from .models import Student, StudentAttendance
from schedule.models import Lesson, LessonInstance
from subjects.models import Subject

import json

def student_grades_view(request, id):

    student = Student.objects.get(id=id)
    grades = Grade.objects.filter(student=student)
    
    lessons = Lesson.objects.filter(class_id = student.class_id)
    dist_lessons = Lesson.objects.filter(class_id = student.class_id).values(
        'class_id',
        'class_id__class_name',
        'class_id__class_letter',
        'class_id__school',
        'teacher_id',
        'subject_id__subject_name',
        'subject_id__id',
        'class_id__id').distinct()

    student_grades = {}
    for lesson in dist_lessons:
        subject = Subject.objects.get(subject_name=lesson['subject_id__subject_name'])
        student_grades[subject.subject_name] = Grade.get_all_student_subject_grades(student, subject)

    context = {
        'student_grades': student_grades,
        'student': student
        }

    return render(request, 'students/student_grades.html', context=context)

def student_attendance_view(request, id):

    student = Student.objects.get(id=id)

    dist_lessons = Lesson.objects.select_related('class_id', 'teacher_id', 'subject_id').filter(class_id=student.class_id).values(
    'class_id__class_name',
    'class_id__class_letter',
    'class_id__school',
    'teacher_id__id',
    'subject_id__subject_name',
    'subject_id__id',
    'class_id__id',
    'sem_1',
    'sem_2'
    )

    print(dist_lessons)

    student_attendances = StudentAttendance.objects.filter(student=student)

    '''
    attendance_values = {
        'subject': {
            '1': {'present': 2, 'absent': 1, 'late': 0},
            '2': {'present': 1, 'absent': 0, 'late': 2},
            'all': {'present': 3, 'absent': 1, 'late': 2}
        }
    }
    '''
    attendance_values = {}

    first_sem_present = 0
    first_sem_absent = 0
    first_sem_late = 0

    second_sem_present = 0
    second_sem_absent = 0
    second_sem_late = 0

    all_present = 0
    all_absent = 0
    all_late = 0

    # count attendances per lesson
    for dist_lesson in dist_lessons:
        subject = Subject.objects.get(subject_name=dist_lesson['subject_id__subject_name'])
        sem_1 = bool(dist_lesson['sem_1'])
        sem_2 = bool(dist_lesson['sem_2'])
        lesson = Lesson.objects.get(class_id = student.class_id, subject_id=subject, sem_1=sem_1, sem_2=sem_2)
        print(lesson)
        lesson_instances = LessonInstance.objects.filter(lesson=lesson)
        # ile obecności razem
        present_count_all = StudentAttendance.objects.filter(student=student, lesson_id__in=lesson_instances.all(), is_present=True).count()
        # ile nieobecności razem
        absent_count_all = StudentAttendance.objects.filter(student=student, lesson_id__in=lesson_instances.all(), is_absent=True).count()
        # ile spóźnień razem
        late_count_all = StudentAttendance.objects.filter(student=student, lesson_id__in=lesson_instances.all(), is_late=True).count()
        # ile obecności 1_sem
        present_count_first_sem = StudentAttendance.objects.filter(student=student, lesson_id__in=lesson_instances.filter(term=1), is_present=True).count()
        # ile nieobecności 1_sem
        absent_count_first_sem = StudentAttendance.objects.filter(student=student, lesson_id__in=lesson_instances.filter(term=1), is_absent=True).count()
        # ile spóźnień 1_sem
        late_count_first_sem = StudentAttendance.objects.filter(student=student, lesson_id__in=lesson_instances.filter(term=1), is_late=True).count()
        # ile obecności 2_sem
        present_count_second_sem = StudentAttendance.objects.filter(student=student, lesson_id__in=lesson_instances.filter(term=2), is_present=True).count()
        # ile nieobecności 2_sem
        absent_count_second_sem = StudentAttendance.objects.filter(student=student, lesson_id__in=lesson_instances.filter(term=2), is_absent=True).count()
        # ile spóźnień 2_sem
        late_count_second_sem = StudentAttendance.objects.filter(student=student, lesson_id__in=lesson_instances.filter(term=2), is_late=True).count()

        attendance_values[dist_lesson['subject_id__subject_name']] = {'all': {'present': present_count_all, 'absent': absent_count_all, 'late': late_count_all},
                                                                      '1': {'present': present_count_first_sem, 'absent': absent_count_first_sem, 'late': late_count_first_sem},
                                                                      '2': {'present': present_count_second_sem, 'absent': absent_count_second_sem, 'late': late_count_second_sem}}
        

        first_sem_present += present_count_first_sem
        first_sem_absent += absent_count_first_sem
        first_sem_late += late_count_first_sem

        second_sem_present += present_count_second_sem
        second_sem_absent += absent_count_second_sem
        second_sem_late += late_count_second_sem

        all_present += present_count_all
        all_absent += absent_count_all
        all_late += late_count_all

        
        


    overall = [[first_sem_present, first_sem_absent, first_sem_late], [second_sem_present, second_sem_absent, second_sem_late], [all_present, all_absent, all_late]]
    
    jsonData = json.dumps(overall)
    

    context = {
        'student_attendances': student_attendances,
        'student': student,
        'attendance_values': attendance_values,
        'jsonData': jsonData,
        'overall': overall
    }

    return render(request, 'students/student_attendance.html', context=context)


def student_report_view(request, id):

    student = Student.objects.get(id=id)

    dist_lessons = Lesson.objects.select_related('class_id', 'teacher_id', 'subject_id').filter(class_id=student.class_id).values(
    'class_id__class_name',
    'class_id__class_letter',
    'class_id__school',
    'teacher_id__id',
    'subject_id__subject_name',
    'subject_id__id',
    'class_id__id'
    )

    student_reports = StudentReport.objects.filter(student=student)
        
    print(student_reports)

    context = {
        'student': student,
        'student_reports': student_reports
    }

    return render(request, 'students/student_reports.html', context=context)