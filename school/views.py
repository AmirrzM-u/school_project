from django.shortcuts import render, redirect, get_object_or_404
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
    news = get_object_or_404(SchoolNews, id=news_id)
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
    user_type = request.user.user_type
    if user_type == 'std':
        user = request.user
        student = user.student_account
        return render(request, 'home/student_profile.html', {'user':user, 'student':student})
    elif user_type == 'prn':
        user = request.user
        student = user.parent_account.children
        return render(request, 'home/student_profile.html', {'user':user, 'student':student})
    elif user_type == 'tch':
        user = request.user
        return render(request, 'home/teacher_profile.html', {'user':user})

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
        if request.user.user_type == 'std':
            student = request.user.student_account
        elif request.user.user_type == 'prn':
            student = request.user.parent_account.children

    except StudentAccount.DoesNotExist:
        raise PermissionDenied('کاربر دانش آموز نمی باشد')
    
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