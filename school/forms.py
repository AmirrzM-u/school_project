from django import forms
from .models import *
from django.contrib.auth import authenticate

class StudentSigninForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label='نام کاربری')
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput, label='رمز عبور')
    student_id = forms.IntegerField(required=True, label='شناسه دانش آموز')

    def clean(self):
        cd = super().clean()
        username = cd.get('username')
        password = cd.get('password')
        student_id = cd.get('student_id')

        if (username and password and student_id):
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('نام کاربری یا رمز عبور اشتباه است')
            if not user.student_account.id_student == student_id:
                raise forms.ValidationError('شناسه کاربری دانش آموز مطابقت ندارد')
            self.user = user
        return cd
    
class TeacherSigninForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label='نام کاربری')
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput, label='رمز عبور')
    teacher_id = forms.IntegerField(required=True, label='شناسه معلم')

    def clean(self):
        cd = super().clean()
        username = cd.get('username')
        password = cd.get('password')
        teacher_id = cd.get('teacher_id')

        if (username and password and teacher_id):
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('نام کاربری یا رمز عبور اشتباه است')
            if not user.teacher_account.id_teacher == teacher_id:
                raise forms.ValidationError('شناسه کاربری مطابقت ندارد')
            self.user = user
        return cd
    
class ParentSigninForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label='نام کاربری')
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput, label='رمز عبور')
    student_id = forms.IntegerField(required=True, label='شناسه دانش آموز شما')

    def clean(self):
        cd = super().clean()
        username = cd.get('username')
        password = cd.get('password')
        student_id = cd.get('student_id')

        if (username and password and student_id):
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('نام کاربری یا رمز عبور اشتباه است')
            if not user.parent_account.children.id_student == student_id:
                raise forms.ValidationError('شناسه کاربری دانش آموز شما مطابقت ندارد')
            self.user = user
        return cd
    
class ParentTicketForm(forms.Form):
    title = forms.CharField(max_length=100, required=True, label='موضوع پیام شما')
    description = forms.CharField(max_length=1000, required=True,widget=forms.Textarea, label='متن پیام شما')

class RecordScore(forms.Form):
    score = forms.DecimalField(max_digits=4, decimal_places=2, max_value=20, min_value=1, label='نمره')

class TicketResponse(forms.Form):
    response = forms.CharField(max_length=1000, label='پاخ پیام')