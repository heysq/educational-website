# -*- coding: utf-8 -*-
# author:Sunqi
from django import forms
from operation.models import UserAsk
import  re

class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        mobile = self.clean_data['mobile']

        moblie_re= '^1[358]\d[9]|^147\d{8}|^176\d{8}$'
        p= re.compile(moblie_re)
        print("111")
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法',code='mobile_invalid')

