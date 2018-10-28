from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic import View
from .models import UserProfile, EmailVerifyRecode
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from django.contrib.auth.hashers import make_password
from utils.email_send import send_register_email
from django.http import HttpResponse,HttpResponseRedirect
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite,UserMessage
from organiation.models import CourseOrg, Teacher
from courses.models import Course
from pure_pagination import EmptyPage, PageNotAnInteger, Paginator
from django.core.urlresolvers import reverse
from users.models import Banner
import json


# Create your views here.
class IndexView(View):
    def get(self,request):
        # print(1/0)
        banners = Banner.objects.all().order_by("index")
        course = Course.objects.filter(is_banner=False)[:6]
        banner_course = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[0:15]
        return  render(request,'html/index.html',
                       {"banners":banners,
                       'banner_course':banner_course,
                        'course':course,
                        'course_orgs':course_orgs,
                        })
class CustomBackend(ModelBackend):
    @classmethod
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    '''类方法'''

    def get(self, request):
        return render(request, 'html/login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", '')
            password = request.POST.get('password', '')
            # user = authenticate(username=user_name, password=password)
            user = CustomBackend.authenticate(request, username=user_name, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'html/login.html',
                              {"msg": "username or password error"})

        else:
            return render(request, 'html/login.html', {"login_form": login_form})


class LogOutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))

'''函数的方法'''


# def login_page(request):

#     if request.method == "POST":
#         user_name = request.POST.get("username", '')
#         password = request.POST.get('password', '')
#         # user = authenticate(username=user_name, password=password)
#         user = CustomBackend.authenticate(request, username=user_name, password=password)
#         if user is not None:
#             login(request, user)
#             return render(request, 'html/index.html', {})
#         else:
#             return render(request, 'html/login.html', {"msg": "username or password error"})
#     elif request.method == "GET":
#         return render(request, 'html/login.html', {})
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {"register_form": register_form}
        return render(request, 'html/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST['email']
            if UserProfile.objects.filter(username=user_name):
                return render(request, 'html/register.html',
                              {"msg": "user already exists", 'register_form': register_form})
            password = request.POST['password']
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(password)
            user_profile.save()
            '''欢迎注册消息'''
            usermessage= UserMessage(user=user_profile.id,message="欢迎注册慕学在线网",has_read=False)
            usermessage.save()
            send_status = send_register_email(user_name, 'register')
            if send_status == 1:
                return HttpResponse("success")

        else:
            return render(request, 'html/register.html', )


class ActiveUserView(View):
    def get(self, request, active_code):
        print(active_code)
        user_code = EmailVerifyRecode.objects.get(code=active_code)
        if user_code:
            user = UserProfile.objects.get(email=user_code.email)
            user.is_active = True
            user.save()
            '''激活成功信息'''
            usermessage = UserMessage(user=user.id,message='邮箱激活成功',has_read=False)
            usermessage.save()
            return HttpResponse('active success')
        else:
            return HttpResponse("active failed")


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'html/forgetpwd.html', {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", '')
            send_status = send_register_email(email, 'forget')
            if send_status == 1:
                return HttpResponse("reset email has send!")
            else:
                return render(request, 'html/forgetpwd.html', {'forget_form': forget_form})


class ResetUserView(View):
    def get(self, request, reset_code):
        all_recodes = EmailVerifyRecode.objects.filter(code=reset_code)
        if all_recodes:
            for code in all_recodes:
                email = code.email
                return render(request, 'html/password_reset.html', {'email': email})
            # return HttpResponse('reset success')
        else:
            return HttpResponse("reset failed")


class ModifyPwdView(View):
    '''修改用户密码'''

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", '')
            pwd2 = request.POST.get("password2", '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'html/password_reset.html', {"email": email, "msg": 'password is not the same'})

            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            usermessage = UserMessage(user=user.id,message="修改密码成功",has_read=False)
            usermessage.save()
            return render(request, 'html/login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'html/password_reset.html', {'email': email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        info_active = True
        return render(request, 'html/usercenter-info.html', {"info_active": info_active})

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()


class UploadImageView(LoginRequiredMixin, View):
    '''用户修改头像'''

    def post(self, request):
        upload_image_form = UploadImageForm(request.POST, request.FILES)
        if upload_image_form.is_valid():
            image = upload_image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            # upload_image_form.save()也可以
            res = {"status": 'success', "msg": "修改成功"}
            return HttpResponse(json.dumps(res), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"status": 'fail', "msg": "修改失败"}), content_type='application/json')


class UpdatePwdView(View):
    '''修改用户密码'''

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", '')
            pwd2 = request.POST.get("password2", '')

            if pwd1 != pwd2:
                return HttpResponse(json.dumps({'status': "fail", 'msg': '密码不一致'}), content_type='application/json')

            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse(json.dumps({'status': 'success', "msg": '修改成功'}), content_type='application/json')
        else:

            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    '''发送邮箱验证码'''

    def get(self, request):
        email = request.GET.get('email', '')
        print(email)
        if UserProfile.objects.filter(email=email):
            return HttpResponse(json.dumps({'email': "邮箱已经存在"}), content_type='application/json')
        send_status = send_register_email(email, send_type='update')
        return HttpResponse(json.dumps({'status': 'success', "msg": "发送成功"}), content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    '''修改个人邮箱'''

    def post(self, request):
        code = request.POST.get('code', '')
        email = request.POST.get('email', '')
        exists_code = EmailVerifyRecode.objects.all().filter(code=code, email=email, send_type='update')
        if exists_code:
            user = request.user
            user.email = email
            user.save()

            return HttpResponse(json.dumps({'status': 'success'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"email": "验证码出错"}), content_type='application/json')


class MyCourseView(View):
    def get(self, request):
        user_course = UserCourse.objects.filter(user=request.user)
        course_active = True
        return render(request, 'html/usercenter-mycourse.html',
                      {"user_course": user_course, "course_active": course_active})


class MyFavOrgView(View):
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(fav_type=2, user=request.user)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'html/usercenter-fav-org.html', {'org_list': org_list})


class MyFavTeacherView(View):
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(fav_type=3, user=request.user)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'html/usercenter-fav-teacher.html', {'teacher_list': teacher_list})


class MyFavCourseView(View):
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(fav_type=1, user=request.user)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'html/usercenter-fav-course.html', {'course_list': course_list})


class MyMessageView(View):
    def get(self,request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        try:
            '''分页'''
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_messages, 5, request=request)
        messages = p.page(page)
        return  render(request,'html/usercenter-message.html',{'messages':messages})



def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('html/404.html',{})
    response.status_code= 404
    return  response


def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('html/500.html',{})
    response.status_code= 500
    return  response