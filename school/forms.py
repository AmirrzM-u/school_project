from django import forms
from .models import *
from django.contrib.auth import authenticate

class SigninForm(forms.Form):
    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
    USER_TYPE_OPTION = (
        ('دانش آموز', 'دانش آموز'),
        ('معلم', 'معلم'),
        ('والدین', 'والدین')
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_OPTION, required=True)

    def clean(self):
        cd = super().clean()
        username = cd.get('username')
        password = cd.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('نام کاربری یا رمز عبور اشتباه است')
            self.user = user
        return cd