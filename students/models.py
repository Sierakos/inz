from django.db import models

from accounts.models import CustomUser
from school.models import Class
from parents.models import Parent
from schedule.models import LessonInstance

# signals
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class Student(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    class_id = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    parent_id = models.ForeignKey(Parent, on_delete=models.SET_NULL, related_name='students', null=True)

    def __str__(self):
        return self.student.last_name + " " + self.student.first_name
    
class StudentAttendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    lesson = models.ForeignKey(LessonInstance, on_delete=models.CASCADE)

    is_present = models.BooleanField(default=True)
    is_absent = models.BooleanField(default=False)
    is_late = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.student.last_name}  {self.student.student.first_name}"
    
    def get_formated_create_at(self):
        return self.created_at.strftime('%d %B %Y - %H:%M')


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if "Student" in instance.user_type:
            Student.objects.create(student=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if "Student" in instance.user_type:
        instance.student.save()

@receiver(post_delete, sender=Student)
def delete_user(sender, instance, **kwargs):
    if instance.student:
        instance.student.delete()