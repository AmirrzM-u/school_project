from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from .models import *
from .forms import *
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden

def getting_studentaccount_from_user(user):
    if user.user_type == 'std':
        return user.student_account
    elif user.user_type == 'prn':
        return user.parent_account.children

FORM_MAP = {
    'student':StudentSigninForm,
    'teacher':TeacherSigninForm,
    'parent':ParentSigninForm,
}

def user_signin(request, user_type):
    form_class = FORM_MAP.get(user_type)
    if form_class:
        form = form_class(request.POST or None)
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
    user_type = request.user.user_type
    user = request.user
    if user_type == 'std' or user_type == 'prn':
        student = getting_studentaccount_from_user(user)
        return render(request, 'home/student_profile.html', {'user':user, 'student':student})
    elif user_type == 'tch':
        return render(request, 'home/teacher_profile.html', {'user':user})
    else:
        raise PermissionDenied('شما مجاز به دسترسی به این صفحه نیستید.')

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
    news = get_object_or_404(SchoolNews, id=news_id)
    return render(request, 'home/school_news.html', {'news':news})

@login_required    
def student_scores(request, grade=None):
    user_type = request.user.user_type
    if user_type == 'std' or user_type == 'prn':
        try:
            student = getting_studentaccount_from_user(request.user)
        except StudentAccount.DoesNotExist:
            raise PermissionDenied('کاربر مجاز نمی باشد')    
    avg_map = {
        '10':student.avg_1,
        '11':student.avg_2,
        '12':student.avg_3,
    }
    grade_map = {
        '10':'دهم',
        '11':'یازدهم',
        '12':'دوازدهم',
    }
    if grade:
        terms = student.term_student.filter(term_lesson__grade_level=grade)
    context = {
        "terms":terms,
        "grade":grade_map[grade],
        "avg":avg_map[grade],
        "student_grade":student.grade_level,
        }
    return render(request, 'home/student_scores.html', context)

@login_required
def student_schedule(request):
    user_type = request.user.user_type
    try:
        if user_type == 'std' or user_type == 'prn':
            student = getting_studentaccount_from_user(request.user)
    except StudentAccount.DoesNotExist:
        raise PermissionDenied('کاربر مجاز نمی باشد')
    
    student_grade = student.grade_level
    student_term = student.term_student.filter(term_lesson__grade_level=student_grade)

    return render(request, 'home/student_schedule.html', {'student_term':student_term})

@login_required
def teacher_panel_for_parents(request):
    parent = request.user
    if parent.user_type != 'prn':
        raise PermissionDenied('شما به این صفحه دسترسی ندایرید')
    student = request.user.parent_account.children
    terms = student.term_student.all()

    context = {
        'parent':parent,
        'student':student,
        'terms':terms,
    }
    return render(request, 'home/teacher_panel_for_parents.html', context)

@login_required
def teacher_profile_for_prn(request, teacher_id):
    parent = request.user
    if request.user.user_type != 'prn':
        raise PermissionDenied('شما به این صفحه دسترسی ندایرید')
    
    teacher = TeacherAccount.objects.get(id_teacher=teacher_id)
    tickets = Ticket.objects.filter(parent=request.user.parent_account, teacher=teacher)
    context = {
        'parent':parent,
        'teacher':teacher,
        'tickets':tickets,
    }
    return render(request, 'home/teacher_profile_for_prn.html', context)

def parent_ticket(request, teacher_id):
    if request.user.user_type != 'prn':
        raise PermissionDenied('شما به این صفحه دسترسی ندایرید')
    parent = request.user.parent_account
    teacher = TeacherAccount.objects.get(id_teacher=teacher_id)
    form = ParentTicketForm(request.POST or None)
    if form.is_valid():
        cd = form.cleaned_data
        ticket = Ticket.objects.create(
            parent = parent,
            teacher = teacher,
            title = cd['title'],
            description = cd['description']
        )
        return redirect('teacher_profile_for_prn', teacher_id)
    return render(request, 'home/parent_ticket.html', {'form':form})

def record_scores(request):
    if request.user.user_type != 'tch':
        raise PermissionDenied('شما به این صفحه دسترسی ندایرید')
    teacher = request.user.teacher_account
    terms = StudentTerm.objects.filter(term_teacher=teacher, active_term=True)
    form = RecordScore(request.POST or None)
    if form.is_valid():
        term_id = request.POST.get('term_id')
        score = form.cleaned_data['score']
        term = StudentTerm.objects.get(id=term_id)
        term.student_score = score
        term.save()
        return redirect('record_scores', )
    return render(request, 'home/record_scores.html', {'teacher':teacher, 'terms':terms, 'form':form})

def ticket_response(request):
    if request.user.user_type != 'tch':
        raise PermissionDenied('شما به این صفحه دسترسی ندایرید')
    teacher = request.user.teacher_account
    tickets = Ticket.objects.filter(teacher=teacher)
    form = TicketResponse(request.POST or None)
    if form.is_valid():
        ticket_id = request.POST.get('ticket_id')
        response = form.cleaned_data['response']
        ticket = Ticket.objects.get(id=ticket_id)
        ticket.response = response
        ticket.status = 'true'
        ticket.save()
        return redirect('ticket_response')
    return render(request, 'home/ticket_response.html', {'tickets':tickets, 'form':form})