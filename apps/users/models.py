from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default='')
    birthday = models.DateTimeField(null=True, verbose_name="生日", blank=True)
    gender = models.CharField(choices=(("male", '男'), ("female", "女")), max_length=6, default='', verbose_name='性别')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机')
    image = models.ImageField(upload_to="image/%y/%m", max_length=100, default="image/default.png")
    address = models.CharField(max_length=100,default='',null=True,verbose_name='地址')

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

    def unread_nums(self,request):
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=request.user.id).count
class EmailVerifyRecode(models.Model):
    code = models.CharField(max_length=20, null=False, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    send_type = models.CharField(choices=(("register", u"注册"), ("forget", u"找回密码"),("update","更新密码")), max_length=10)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.code


class Banner(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="banner/%y/%m", verbose_name=u"轮播图")
    url = models.URLField(max_length=200,verbose_name='访问地址')
    index = models.IntegerField(default=100, verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name="轮播图"
        verbose_name_plural= verbose_name
