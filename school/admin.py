from django.contrib import admin
from .models import School, Class, Specjalization, Subject

# Register your models here.
admin.site.register(School)
admin.site.register(Class)
admin.site.register(Specjalization)
admin.site.register(Subject)