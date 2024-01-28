from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
from students.models import Student
from schedule.models import Lesson
from teachers.models import Teacher
from subjects.models import Subject
from school.models import Class

class Assigment(models.Model):
    name = models.CharField(max_length=200)
    weight = models.IntegerField(default=1)

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

    
