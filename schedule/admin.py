from django.contrib import admin
from .models import Lesson, LessonInstance

class LessonAdmin(admin.ModelAdmin):
    exclude = ['start_time', 'end_time']

admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonInstance)