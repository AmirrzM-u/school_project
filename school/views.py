from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from .models import *

def home(request):
    school_news = SchoolNews.objects.all()
    students_number = StudentAccount.objects.all().count()
    class_numbers = Classroom.objects.all().count()
    teachers_number = TeacherAccount.objects.all().count()

    context = {
        'school_news': school_news,
        'student_number': students_number,
        'class_number': class_numbers,
        'teachers_number': teachers_number,
    }

    return render(request, "base/home.html", context)

    
    
