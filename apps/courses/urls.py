# -*- coding: utf-8 -*-
# author:Sunqi
from django.conf.urls import  url,include
from operation.views import CourseListView,CourseDetailView,CourseInfoView,CommentView,AddCommentView


urlpatterns = [
    url(r'^list/$',CourseListView.as_view(),name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$',CourseInfoView.as_view(),name='course_info'),
    url(r'^comment/(?P<course_id>\d+)/$',CommentView.as_view(),name='course_comment'),
    url(r'^add_comment/$',AddCommentView.as_view(),name='add_comment'),

]
