# -*- coding: utf-8 -*-
# author:Sunqi
from django.conf.urls import url
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, \
    MyFavOrgView, MyFavTeacherView, MyFavCourseView,MyMessageView

urlpatterns = [
    # '''用户信息'''
    url(r'info/', UserInfoView.as_view(), name="info"),
    # 用户头像上传
    url(r'image/upload/', UploadImageView.as_view(), name="image_upload"),
    # '''修改密码'''
    url(r'update/pwd/', UpdatePwdView.as_view(), name="update_pwd"),
    # '''发送验证码'''
    url(r'sendemail_code/', SendEmailCodeView.as_view(), name="sendemail_code"),
    # '''修改邮箱'''
    url(r'update_email/', UpdateEmailView.as_view(), name="update_email"),
    # '''我的课程'''
    url(r'my_couese/', MyCourseView.as_view(), name="my_course"),
    # 我的收藏课程机构
    url(r'my_fav/org/', MyFavOrgView.as_view(), name="my_fav_org"),
    # 我的收藏讲师
    url(r'my_fav/teacher/', MyFavTeacherView.as_view(), name="my_fav_teacher"),
    # 我的收藏课程
    url(r'my_fav/course/', MyFavCourseView.as_view(), name="my_fav_course"),
    # 我的消息
    url(r'my_message/', MyMessageView.as_view(), name="my_message"),

]
