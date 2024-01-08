from django.db import models
from django.contrib.auth.models import AbstractUser

# signals
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE = (("Admin", "Admin"), ("Staff", "Staff"), ("Teacher", "Teacher"), ("Student", "Student"), ("Parent", "Parent"))
    GENDER = [("M", "Male"), ("F", "Female")]

    user_type = models.CharField(default=1, choices=USER_TYPE, max_length=10)
    gender = models.CharField(max_length=1, choices=GENDER)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.last_name + ", " + self.first_name
    
class Admin(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin.last_name + ", " + self.admin.first_name

class Staff(models.Model):
    staff = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.staff.last_name + " " + self.staff.first_name
    
class Teacher(models.Model):
    teacher = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.teacher.last_name + " " + self.teacher.first_name

class Student(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    course = models.TextField()

    def __str__(self):
        return self.student.last_name + " " + self.student.first_name

class Parent(models.Model):
    parent = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.parent.last_name + " " + self.parent.first_name

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == "Admin":
            Admin.objects.create(admin=instance)
        if instance.user_type == "Staff":
            Staff.objects.create(staff=instance)
        if instance.user_type == "Teacher":
            Teacher.objects.create(teacher=instance)
        if instance.user_type == "Student":
            Student.objects.create(student=instance)
        if instance.user_type == "Parent":
            Parent.objects.create(parent=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == "Admin":
        instance.admin.save()
    if instance.user_type == "Staff":
        instance.staff.save()
    if instance.user_type == "Teacher":
        instance.teacher.save()
    if instance.user_type == "Student":
        instance.student.save()
    if instance.user_type == "Parent":
        instance.parent.save()
