from django.contrib import admin
from .models import School, Class, Classroom, Term, SubjectTerm


# Register your models here.
admin.site.register(School)
admin.site.register(Class)
admin.site.register(Classroom)
admin.site.register(Term)
admin.site.register(SubjectTerm)
