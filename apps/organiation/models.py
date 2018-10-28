from django.db import models
from datetime import datetime
from courses.models import *


# Create your models here.

class CityDict(models.Model):
    name = models.CharField(max_length=50, verbose_name="城市名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    desc = models.TextField(verbose_name="城市描述")

    class Meta:
        verbose_name = "公司名"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"机构名称")
    desc = models.TextField(verbose_name=u"机构描述")
    category = models.CharField(max_length=20,choices=(("pxjg","培训机构"),("gx","高校"),("gr","个人")),verbose_name="机构类别",default="pxjg")
    address = models.CharField(max_length=150, verbose_name=u"机构地址")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    image = models.ImageField(upload_to="org/%y/%m", max_length=100, verbose_name=u"封面图")
    city = models.ForeignKey(CityDict, verbose_name=u"所在城市", on_delete=models.CASCADE)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    students = models.IntegerField(default=0,verbose_name="学习人数")
    course_nums = models.IntegerField(default=0,verbose_name='课程数')
    class Meta:
        verbose_name = u"课程机构"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u"所属机构", on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name=u"教师名称")
    age = models.IntegerField(default=0,verbose_name='教师年龄')
    work_years = models.IntegerField(default=0, verbose_name=u"工作年限")
    work_company = models.CharField(max_length=100, verbose_name=u"就职公司")
    work_position = models.CharField(max_length=100, verbose_name=u"公司职位")
    image = models.ImageField(max_length=100,upload_to='teacher/%Y/%m',verbose_name="教师照片",null=True)
    class_course = models.CharField(max_length=100,default='',null=True,verbose_name="经典课程")
    points = models.CharField(max_length=50, verbose_name=u"教学特点")
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
