from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, ListView, DetailView
from .models import *
from .forms import *
from django.contrib.auth import login, logout

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

def news_detail(request, news_id):
    news = SchoolNews.objects.get(id=news_id)
    return render(request, 'home/school_news.html', {'news':news})

def user_signin(request):
    form = SigninForm(request.POST or None)
    if form.is_valid():
        login(request, form.user)
        return render('home')
    return render(request, 'registration/login.html', {'form':form})



    
    
