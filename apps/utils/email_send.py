# -*- coding: utf-8 -*-
# author:Sunqi
import  random
from users.models import EmailVerifyRecode
from django.core.mail import send_mail
from untitled.settings import EMAIL_FROM

def send_register_email(email,send_type="register"):
    email_recode = EmailVerifyRecode()
    code = get_code(8)
    email_recode.code =  code
    email_recode.email = email
    email_recode.send_type = send_type
    email_recode.save()
    email_title = ''
    email_body = ''
    if send_type=="register":
        email_title="注册账户激活链接"
        email_body = '点击以下链接激活账户http://127.0.0.1:8000/active/{0}'.format(code)
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email,])
        return send_status
    if send_type=="forget":
        email_title = "注册账户重置链接"
        email_body = '点击以下链接重置账户http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email, ])
        return send_status
    if send_type=="update":
        email_title = "修改密码验证码"
        email_body = '你的邮箱验证码为：  {0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email, ])
        return send_status




def get_code(randomlength):
    chars = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
    length = len(chars)-1
    str = ""
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str