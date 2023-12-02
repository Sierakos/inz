from django.db import models
from school.models import Class, School, Subject


class Lesson(models.Model):
    DAY_CHOICES = [
        ('Poniedziałek', 'Poniedziałek'),
        ('Wtorek', 'Wtorek'),
        ('Środa', 'Środa'),
        ('Czwartek', 'Czwartek'),
        ('Piątek', 'Piątek'),
    ]

    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE)
    # teacher_id
    # room_id
    day = models.CharField(max_length=12, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.class_id} {self.subject_id} {self.day} {self.start_time} - {self.end_time}"

