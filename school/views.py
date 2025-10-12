from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView, ListView, DetailView
from .models import *
from .forms import *
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


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

@login_required
def user_profile(request):
    user = request.user
    user_type = user.user_type
    if user_type == 'std':
        return render(request, 'home/student_profile.html', {'user':user})
    elif user_type == 'prn':
        return render(request, 'home/student_profile.html', {'user':user})



@login_required    
def student_scores(request):
    if request.user.user_type == 'std':
        try:
            student = request.user.student_account
        except StudentAccount.DoesNotExist:
            raise PermissionDenied('کاربر دانش آموز نمی باشد')
        student_term = student.term_student

    if request.user.user_type == 'prn':
        try:
            student = request.user.parent_account.children
        except StudentAccount.DoesNotExist:
            raise PermissionDenied('کاربر دانش آموز نمی باشد')
        student_term = student.term_student

    grade_10 = student_term.filter(term_lesson__grade_level = '10')
    scores_1 = [term.student_score for term in grade_10]
    avg_1 = sum(scores_1) / len(scores_1) if scores_1 else 0

    grade_11 = student_term.filter(term_lesson__grade_level = '11')
    scores_2 = [term.student_score for term in grade_11]
    avg_2 = sum(scores_2) / len(scores_2) if scores_2 else 0
    
    grade_12 = student_term.filter(term_lesson__grade_level = '12')
    scores_3 = [term.student_score for term in grade_12]
    avg_3 = sum(scores_3) / len(scores_3) if scores_3 else 0

    student.avg_1 = avg_1
    student.avg_2 = avg_2
    student.avg_3 = avg_3
    
    student.save(update_fields=['avg_1', 'avg_2', 'avg_3'])

    if student.grade_level == '10':
        context = {
            'student': student,
            'student_term':student_term,
            'grade_10':grade_10,
        }
    elif student.grade_level == '11':
        context = {
            'student': student,
            'student_term':student_term,
            'grade_10':grade_10,
            'grade_11':grade_11
        }
    elif student.grade_level == '12':
        context = {
            'student': student,
            'student_term':student_term,
            'grade_10':grade_10,
            'grade_11':grade_11,
            'grade_12':grade_12
        }

    return render(request, 'home/student_scores.html', context)

@login_required
def student_schedule(request):
    try:
        student = request.user.student_account
    except StudentAccount.DoesNotExist:
        raise PermissionDenied('کاربر دانش آموز نمی باشد')
    
    student_grade = student.grade_level
    student_term = student.term_student.filter(term_lesson__grade_level=student_grade)

    return render(request, 'home/student_schedule.html', {'student_term':student_term})

@login_required
def teacher_panel_for_parents(request):
    student = request.user.parent_account.children
    term = student.term_student.all()
    return render(request, 'home/teacher_panel_for_parents.html')
  
