from django.db import models

# Create your models here.
from students.models import Student
from schedule.models import Lesson
from teachers.models import Teacher
from subjects.models import Subject
from school.models import Class

class Assigment(models.Model):
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    weight = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.subject_id} - {self.name}"

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    assigment = models.ForeignKey(Assigment, on_delete=models.CASCADE)

    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.assigment} - {self.value}"



    
