from django.db import models
from school.models import Class, School, Classroom, Term
from teachers.models import Teacher
from subjects.models import Subject

from datetime import datetime, timedelta, timezone

from django.core.exceptions import ValidationError

import uuid


class Lesson(models.Model):
    DAY_CHOICES = [
        ('Poniedziałek', 'Poniedziałek'),
        ('Wtorek', 'Wtorek'),
        ('Środa', 'Środa'),
        ('Czwartek', 'Czwartek'),
        ('Piątek', 'Piątek'),
    ]

    LESSON_HOURS_CHOICES = [
        ('8:00-8:45', '8:00-8:45'),
        ('8:50-9:35', '8:50-9:35'),
        ('9:45-10:30', '9:45-10:30'),
        ('10:40-11:25', '10:40-11:25'),
        ('12:40-13:25', '12:40-13:25'),
        ('13:35-14:10', '13:35-14:10'),
        ('14:15-15:00', '14:15-15:00'),
        ('15:05-15:50', '15:05-15:50'),
    ]

    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subject, on_delete=models.CASCADE) #
    teacher_id = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True) #
    room_id = models.ForeignKey(Classroom, on_delete=models.CASCADE) #
    term_id = models.ForeignKey(Term, on_delete=models.CASCADE)
    day = models.CharField(max_length=12, choices=DAY_CHOICES)
    lesson_hours = models.CharField(max_length=12, choices=LESSON_HOURS_CHOICES)
    start_time = models.TimeField(null=True, blank=True) #
    end_time = models.TimeField(null=True, blank=True) #
    sem_1 = models.BooleanField(default=False)
    sem_2 = models.BooleanField(default=False)

    unique_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.class_id} {self.subject_id} {self.day} {self.start_time} - {self.end_time} / {self.term_id}"
    
    def get_formated_day(self):
        return self.day.strftime('%d %B %Y')
    
    def get_formated_start_time(self):
        return self.start_time.strftime('%H:%M')
    
    def get_formated_end_time(self):
        return self.end_time.strftime('%H:%M')
    
    @classmethod
    def get_lessons_with_correct_term(cls, id):
        current_date = datetime.now()
        formated_current_date = current_date.strftime("%Y-%m-%d")

        print(formated_current_date)
        return cls.objects.filter(class_id = id)
    
    def save(self, *args, **kwargs):

        # Przekonwertuj lesson_hours na start_time i end_time
        start_time_str, end_time_str = self.lesson_hours.split('-')
        self.start_time = datetime.strptime(start_time_str, '%H:%M').time()
        self.end_time = datetime.strptime(end_time_str, '%H:%M').time()
        super().save(*args, **kwargs)

        start_date_sem_1 = self.term_id.term_start_sem_1
        end_date_sem_1 = self.term_id.term_end_sem_1

        start_date_sem_2 = self.term_id.term_start_sem_2
        end_date_sem_2 = self.term_id.term_end_sem_2

        
        current_date = start_date_sem_1

        # tworzenie zajęć dla pierwszego semestru
        dates = []
        
        if not LessonInstance.objects.filter(lesson_uuid=self.unique_uuid).exists() and self.sem_1: 
            while current_date <= end_date_sem_1:
                if self.day.lower() == current_date.strftime('%A'):
                    dates.append(current_date)
                    LessonInstance.objects.create(
                        lesson=self,
                        lesson_day=current_date,
                        lesson_start_time=self.start_time,
                        lesson_end_time=self.end_time,
                        term=1,
                        lesson_uuid=self.unique_uuid
                    )
                    
                current_date += timedelta(days=1)

        current_date = start_date_sem_2

        if not LessonInstance.objects.filter(lesson_uuid=self.unique_uuid).exists() and self.sem_2: 
            while current_date <= end_date_sem_2:
                if self.day.lower() == current_date.strftime('%A'):
                    dates.append(current_date)
                    LessonInstance.objects.create(
                        lesson=self,
                        lesson_day=current_date,
                        lesson_start_time=self.start_time,
                        lesson_end_time=self.end_time,
                        term=2,
                        lesson_uuid=self.unique_uuid
                    )
                    
                current_date += timedelta(days=1)

        print(dates)

    def clean(self):
        # Przekonwertuj lesson_hours na start_time i end_time
        start_time_str, end_time_str = self.lesson_hours.split('-')
        start_time = datetime.strptime(start_time_str, '%H:%M').time()
        end_time = datetime.strptime(end_time_str, '%H:%M').time()

        if self.teacher_id and self.day and start_time:
            conflicting_lessons = Lesson.objects.filter(
                teacher_id=self.teacher_id,
                day=self.day,
                start_time=start_time
            ).exclude(id=self.id) # do wykluczenia te właśnie dodawaną lekcje

            if conflicting_lessons.exists():
                raise ValidationError('Nauczyciel jest już przypisany do zajęć w tym dniu i godzinie.')
            
        if self.class_id and self.day and start_time:
            conflicting_lessons = Lesson.objects.filter(
                class_id=self.class_id,
                day=self.day,
                start_time=start_time
            ).exclude(id=self.id)

            if conflicting_lessons.exists():
                raise ValidationError('Ta klasa ma już zajęcia w tym dniu i godzinie.')
            
        if self.room_id and self.day and start_time:
            conflicting_lessons = Lesson.objects.filter(
                room_id=self.room_id,
                day=self.day,
                start_time=start_time
            ).exclude(id=self.id)

            if conflicting_lessons.exists():
                raise ValidationError('Ta sala jest już zajęta w tym dniu i godzinie.')


'''
Próba oddzielenia lekcji od instancji lekcji.

Zamierzane jest tutaj umieszczać osobne dane dla każdej jednej lekcji
(np osobno dla matematyki z poniedziałku czwartku i kolejnego poniedziałku).
Ma to pomóc w oddzieleniu informacji o każdym jednym zajęciu co z kolei skutkuje
usprawnieniem działania systemu sprawdzania obecności.
'''

class LessonInstance(models.Model):
    DAY_CHOICES = [
        ('Poniedziałek', 'Poniedziałek'),
        ('Wtorek', 'Wtorek'),
        ('Środa', 'Środa'),
        ('Czwartek', 'Czwartek'),
        ('Piątek', 'Piątek'),
    ]
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    lesson_day = models.DateField()
    lesson_start_time = models.TimeField()
    lesson_end_time = models.TimeField()
    term = models.IntegerField()

    # przypisanie do danych zajęć
    lesson_uuid = models.UUIDField(editable=False, unique=False)

    is_started = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.lesson.class_id} {self.lesson_day} {self.lesson_start_time} - {self.lesson_end_time}"
    
    def get_formated_day(self):
        return self.lesson_day.strftime('%d %B %Y')
    
    def get_formated_start_time(self):
        return self.lesson_start_time.strftime('%H:%M')
    
    def get_formated_end_time(self):
        return self.lesson_end_time.strftime('%H:%M')

    

