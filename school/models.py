from django.db import models

# Create your models here.

class School (models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100, unique=False)
    post_code = models.CharField(max_length=10, unique=False)
    address = models.TextField(max_length=200, unique=False)

    def __str__(self):
        return self.name
    
class Specjalization(models.Model):
    Specjalization_name = models.CharField(max_length=50)
    school = models.ForeignKey(School, on_delete=models.CASCADE)

    def __str__(self):
        return self.Specjalization_name
    
class Class(models.Model):
    CLASS_CHOICES = [
        ('1', 'Klasa 1'),
        ('2', 'Klasa 2'),
        ('3', 'Klasa 3'),
        ('4', 'Klasa 4'),
        ('5', 'Klasa 5')
    ]

    CLASS_LETTER_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D')
    ]

    class_name = models.CharField(max_length=10, choices=CLASS_CHOICES)
    class_letter = models.CharField(max_length=1, choices=CLASS_LETTER_CHOICES)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specjalization, blank=True, null=True, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.class_name} {self.class_letter} - {self.school}"

class Subject(models.Model):
    subject_name = models.CharField(max_length=50)

    def __str__(self):
        return self.subject_name


