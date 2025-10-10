from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import *
from .forms import *
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


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

def user_signin(request, user_type):
    if user_type == 'student':
        form = StudentSigninForm(request.POST or None)
        if form.is_valid():
            login(request, form.user)
            return redirect('home')
        return render(request, 'registration/login.html', {'form':form})
    elif user_type == 'teacher':
        form = TeacherSigninForm(request.POST or None)
        if form.is_valid():
            login(request, form.user)
            return redirect('home')
        return render(request, 'registration/login.html', {'form':form})
    elif user_type == 'parent':
        form = ParentSigninForm(request.POST or None)
        if form.is_valid():
            login(request, form.user)
            return redirect('home')
        return render(request, 'registration/login.html', {'form':form})        

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def user_profile(request):
    user = request.user
    return render(request, 'home/profile.html', {'user':user})
    
    
