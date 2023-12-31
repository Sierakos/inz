from django.shortcuts import render
from .models import Lesson
import json

# Create your views here.

def index(request, id):
    lessons = Lesson.objects.filter(class_id=id)
    data = {}
    for lesson in lessons:
        data[str(lesson.id)] = {
            "name": lesson.subject_id.subject_name, 
            "datatime": [lesson.day, lesson.start_time.hour, lesson.start_time.minute, lesson.end_time.hour, lesson.end_time.minute]
        }

    jsonData = json.dumps(data)
    print(jsonData)


    return render(request, 'schedule/index.html', {
        'jsonData': jsonData
        })