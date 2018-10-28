from django.db import models

# Create your models here.
from datetime import datetime
from organiation.models import CourseOrg
from organiation.models import Teacher

class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, null=True, blank=True, verbose_name="课程机构")
    name = models.CharField(max_length=50, verbose_name=u"课程名称")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    degree = models.CharField(choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=3, verbose_name=u"难度")
    learn_time = models.IntegerField(default=0, verbose_name=u"学习时长")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to='courses/%Y/m', verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u'点击量')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    category = models.CharField(max_length=20, verbose_name='课程类别', null=True)
    tag = models.CharField(max_length=10,default='',verbose_name="课程标签")
    teacher = models.ForeignKey(Teacher,verbose_name='讲师',on_delete=models.CASCADE,null=True,blank=True)
    is_banner = models.BooleanField(default=False,verbose_name="是否是轮播图")
    youneed_know = models.CharField(max_length=200,verbose_name="教师提醒",default="")
    teahcher_tell = models.CharField(max_length=100,verbose_name="学到什么",null=True)
    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def get_zj_nums(self):
        '''获取课程章节数'''
        return self.lesson_set.all().count()
    get_zj_nums.short_description = "章节数"

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href = 'http://www.baidu.com'>跳转</a>")
    go_to.short_description = '跳转'
    def get_course_lessong(self):
        '''获取课程章节'''
        return self.lesson_set.all()

    def learn_course_nums(self):
        return self.usercourse_set.all()[:5]


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"章节名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True#不设置为true 会再生成一张表
class Vedio(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"视频名称")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    url = models.CharField(max_length=100, default='', verbose_name="访问地址")
    play_time = models.IntegerField(default=0,verbose_name="视频时长")
    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y/m", verbose_name=u"课程下载", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name
