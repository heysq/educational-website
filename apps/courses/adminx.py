# -*- coding: utf-8 -*-
# author:Sunqi
import xadmin
from .models import Course,Lesson,Vedio,CourseResource,BannerCourse
from organiation.models import CourseOrg

class LessonInline():
    model= Lesson
    extra = 0


class CourseAdmin():
    list_display = ['id','name', 'desc', 'degree', 'learn_time', 'students', 'fav_nums', 'image', "click_nums", 'add_time','get_zj_nums','go_to']
    search_fields = ['name', 'desc', 'degree', 'learn_time', 'students', 'fav_nums', 'image', "click_nums", ]
    list_filter = ['name', 'desc', 'degree', 'learn_time', 'students', 'fav_nums', 'image', "click_nums", 'add_time']
    inlines= [LessonInline,]
    # readonly_fields = ["click_nums",'fav_nums']更改字段只读
    #exclude = ['fav_nums']隐藏字段，与只读冲突
    def save_model(self):
        '''保存课程的时候课程机构机构的课程数加1'''
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org = course_org).count()
            course_org.save()

class BannerCourseAdmin():
    list_display = ['id','name', 'desc', 'degree', 'learn_time', 'students', 'fav_nums', 'image', "click_nums", 'add_time']
    search_fields = ['name', 'desc', 'degree', 'learn_time', 'students', 'fav_nums', 'image', "click_nums", ]
    list_filter = ['name', 'desc', 'degree', 'learn_time', 'students', 'fav_nums', 'image', "click_nums", 'add_time']
    inlines= [LessonInline,]
    # readonly_fields = ["click_nums",'fav_nums']更改字段只读
    #exclude = ['fav_nums']隐藏字段，与只读冲突


class CourseResourceAdmin():
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download', ]
    list_filter = ['course', 'name', 'download', 'add_time']


class LessonAdmin():
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course', 'name', 'add_time']


class VedioAdmin():
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Vedio,VedioAdmin)
