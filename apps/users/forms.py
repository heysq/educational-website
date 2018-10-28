# -*- coding: utf-8 -*-
# author:Sunqi
from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True, max_length=5)
    password = forms.CharField(required=True)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True)
    captchas = CaptchaField(error_messages={"invalid": '验证码错误'})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captchas = CaptchaField(error_messages={"invalid": '验证码错误'})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields=['image']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields=["nick_name","birthday",'gender','address','mobile']

