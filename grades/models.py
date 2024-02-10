from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from .utils import *


# Create your models here.
from students.models import Student
from schedule.models import Lesson
from teachers.models import Teacher
from subjects.models import Subject
from school.models import Class

class Assigment(models.Model):
    name = models.CharField(max_length=200)
    weight = models.IntegerField(default=1)

    midterm_grade = models.BooleanField(default=False)
    final_grade = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class Grade(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    assigment = models.ForeignKey(Assigment, null=True, blank=True, on_delete=models.CASCADE)

    value = models.FloatField()
    description = models.CharField(max_length=255, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # convert values:
        CONVERTED_VALUES = {"-": 0, "1": 1, "1+": 1.25, "2-": 1.75, "2": 2, "2+": 2.25, "3-": 2.75, "3": 3, "3+": 3.25,
                             "4-": 3.75, "4": 4, "4+": 4.25, "5-": 4.75, "5": 5, "5+": 5.25, "6-": 5.75, "6": 6} 

        if type(self.value == str):
            self.value = CONVERTED_VALUES[self.value]
        super().save(*args, **kwargs)

    @staticmethod
    def get_all_student_subject_grades(student, subject):
        student_grades = Grade.objects.filter(student=student, subject=subject, assigment__midterm_grade=False, assigment__final_grade=False)

        if Grade.objects.filter(student=student, subject=subject, assigment__midterm_grade=True).exists():
            midterm_grade = Grade.objects.get(student=student, subject=subject, assigment__midterm_grade=True).value
        else:
            midterm_grade = 0

        if Grade.objects.filter(student=student, subject=subject, assigment__final_grade=True).exists():
            final_grade = Grade.objects.get(student=student, subject=subject, assigment__final_grade=True).value
        else:
            final_grade = 0

        term_grades = [midterm_grade, final_grade]
        grades = []
        for student_grade in student_grades:
            conv_value = 0
            if student_grade.value % 1 == 0.25:
                conv_value = f"{int(student_grade.value)}+"
            elif student_grade.value % 1 == 0.75:
                conv_value = f"{int(student_grade.value) + 1}-"
            else:
                conv_value = f"{int(student_grade.value)}"
            grades.append(conv_value)

        return grades, term_grades


    @staticmethod
    def get_avarage_grade(student, subject, term):
        student_grades = Grade.objects.filter(student=student, subject=subject, assigment__midterm_grade=False, assigment__final_grade=False)

        if Grade.objects.filter(student=student, subject=subject, assigment__midterm_grade=True).exists():
            midterm_grade = Grade.objects.get(student=student, subject=subject, assigment__midterm_grade=True).value   
        else:
            midterm_grade = 0

        if Grade.objects.filter(student=student, subject=subject, assigment__final_grade=True).exists():
            final_grade = Grade.objects.get(student=student, subject=subject, assigment__final_grade=True).value
        else:
            final_grade = 0

        ### dla srednich z semestrów
        first_term_grade_sum = 0
        first_term_weight_sum = 0
        second_term_grade_sum = 0
        second_term_weight_sum = 0

        first_term_avarage = 0
        second_term_avarage = 0

        ### dla ogólnej średniej z całego roku
        grade_sum = 0
        weight_sum = 0

        avarage = 0

        for grade in student_grades:
            convert_grade_date = grade.created_at.date()

            grade_sum += (grade.value * grade.assigment.weight)
            weight_sum += grade.assigment.weight

            if (between(convert_grade_date, term.term_start_sem_1, term.term_end_sem_1)):
                first_term_grade_sum += (grade.value * grade.assigment.weight)
                first_term_weight_sum += grade.assigment.weight
            elif (between(convert_grade_date, term.term_start_sem_2, term.term_end_sem_2)):
                second_term_grade_sum += (grade.value * grade.assigment.weight)
                second_term_weight_sum += grade.assigment.weight

        if first_term_weight_sum > 0:
            first_term_avarage = (first_term_grade_sum / first_term_weight_sum)
        if second_term_weight_sum > 0:
            second_term_avarage = (second_term_grade_sum / second_term_weight_sum)

        if weight_sum > 0:
            avarage = (grade_sum / weight_sum)
            
        return [round(first_term_avarage,2), round(second_term_avarage,2), round(avarage,2), midterm_grade, final_grade]
    
    @staticmethod
    def get_avarage_grade_without_term(student, subject):
        student_grades = Grade.objects.filter(student=student, subject=subject, assigment__midterm_grade=False, assigment__final_grade=False)

        ### dla ogólnej średniej z całego roku
        grade_sum = 0
        weight_sum = 0

        avarage = 0

        for grade in student_grades:
            grade_sum += (grade.value * grade.assigment.weight)
            weight_sum += grade.assigment.weight

        if weight_sum > 0:
            avarage = (grade_sum / weight_sum)
            
        return round(avarage,2)

        



    def display_value(self):
        if self.value % 1 == 0.25:
            return f"{int(self.value)}+"
        elif self.value % 1 == 0.75:
            return f"{int(self.value) + 1}-"
        else:
            return f"{int(self.value)}"
        
    def display_created_at_date(self):
        date = self.created_at.date()
        return date.strftime("%d-%m-%Y")
    
    def display_updated_at_date(self):
        date = self.updated_at.date()
        return date.strftime("%d-%m-%Y")
    
    def get_created_month(self):
        date = self.created_at.month
        return date

    def __str__(self):
        return f"{self.student} - {self.assigment} - {self.value}"

class StudentReport(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    report = models.TextField(max_length=500, null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.teacher} -> {self.student} na {self.subject}"
    
    def get_formated_created_at(self):
        return self.created_at.strftime('%d %B %Y - %H:%M')
    
    def get_formated_updated_at(self):
        return self.updated_at.strftime('%d %B %Y - %H:%M')
    
    
