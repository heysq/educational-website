"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
import xadmin
from users.views import LoginView,RegisterView,ActiveUserView,ForgetPwdView,ResetUserView,ModifyPwdView,LogOutView,IndexView
from django.views.generic import  TemplateView
from django.views.static import serve
import captcha
from .settings import  MEDIA_ROOT
from organiation import urls as org_urls
from courses import  urls as course_urls
from users import  urls as user_urls
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^login/$',LoginView.as_view() ,name='login'),
    url(r'^logout/$',LogOutView.as_view() ,name='logout'),
    url(r'^register/$',RegisterView.as_view() ,name='register'),
    url(r"^$",IndexView.as_view(),name='index'),
    url(r'^captcha/',include('captcha.urls')),
    url(r'^active/(?P<active_code>.*$)',ActiveUserView.as_view(),name='active'),
    url(r'^reset/(?P<reset_code>.*$)',ResetUserView.as_view(),name='reset'),
    url(r'^modify_pwd/$',ModifyPwdView.as_view(),name='modify_pwd'),
    url(r'^forget/$',ForgetPwdView.as_view(),name="forget"),
    #课程机构url
    # url(r'^org_list/$',OrgView.as_view(),name='org_list'),
    url(r'^org/',include(org_urls,namespace='org')),
    #上传文件的访问处理函数
    url(r'^media/(?P<path>.*)$',serve,{'document_root':MEDIA_ROOT}),
    # 生产模式服务器静态文件url
    # url(r'^static/(?P<path>.*)$',serve,{'document_root':STATIC_ROOT}),
    # 课程相关url
    url(r'^course/',include(course_urls,namespace='course')),
    # 教师相关url
    # url(r'^teacher/',include(course_urls,namespace='course')),
    # 用户相关url
    url(r'^users/',include(user_urls,namespace='users')),
]
handler404 = "users.views.page_not_found"
handler500 = "users.views.page_error"
