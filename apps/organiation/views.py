from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict
from pure_pagination import EmptyPage, PageNotAnInteger, Paginator
from .forms import UserAskForm
from django.http import HttpResponse
from courses.models import Course, Teacher
from operation.models import UserFavorite
from django.db.models import Q
import json


# Create your views here.
class OrgView(View):
    '''课程机构列表功能'''

    def get(self, request):
        '''课程机构'''
        all_orgs = CourseOrg.objects.all()
        current_nav = 'course_org'
        hot_orgs = all_orgs.order_by("click_nums")[0:3]
        '''城市名称'''
        all_citys = CityDict.objects.all()
        '''机构搜索'''
        keywords = request.GET.get('keywords', '')
        if keywords:
            all_orgs = all_orgs.filter(
                Q(name__icontains=keywords) or
                Q(desc__icontains=keywords))

        cityid = request.GET.get("city", '')
        leibie = request.GET.get('ct', '')
        sort_way = request.GET.get('sort', 'default')
        if sort_way == "default":
            all_orgs = all_orgs
        elif sort_way == "students":
            all_orgs = all_orgs.order_by("students")
        else:
            all_orgs = all_orgs.order_by("course_nums")
        if leibie:
            all_orgs = all_orgs.filter(category=leibie)
        if cityid:
            all_orgs = all_orgs.filter(city_id=int(cityid))
        org_num = all_orgs.count()
        try:
            '''分页'''
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 5, request=request)
        orgs = p.page(page)

        return render(request, 'html/org-list.html', {
            'all_orgs': orgs,
            'all_citys': all_citys,
            'org_num': org_num,
            'city_id': cityid,
            "leibie": leibie,
            'hot_org': hot_orgs,
            'current_nav': current_nav,

        })


class AddUserAskView(View):
    """
    用户添加咨询
    """

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse(json.dumps({"status": "success"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({"status": "fail", "msg": "添加出错"}), content_type='application/json')


class OrgHomeView(View):
    '''机构首页'''

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()
        if course_org:
            all_courses = course_org.course_set.all()
            all_teachers = course_org.teacher_set.all()
            return render(request, 'html/org-detail-homepage.html',
                          {"all_courses": all_courses,
                           "all_teachers": all_teachers,
                           'course_org': course_org,

                           })
            # return render(request,'html/test.html',{'all_courses':all_courses})
        else:
            return HttpResponse("null")


class OrgCourseView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        if course_org:
            all_courses = course_org.course_set.all()
            return render(request, 'html/org-detail-course.html',
                          {"all_courses": all_courses,
                           'course_org': course_org
                           })


class OrgDescView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        if course_org:
            return render(request, 'html/org-detail-desc.html',
                          {
                              'course_org': course_org
                          })


class OrgTeacherView(View):
    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        if course_org:
            return render(request, 'html/org-detail-teachers.html',
                          {
                              'all_teachers': all_teachers
                          })


class AddFavView(View):
    def post(self, request, org_id):
        '''用户收藏与取消'''
        fav_id = request.POST.get("fav_id", 0)
        fav_type = request.POST.get('fav_type', 0)
        if not request.user.is_authenticated():
            '''未登录'''
            return HttpResponse(json.dumps({'status': 'fail', "msg": "用户为登录"}), content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request, fav_id=int(fav_id), fav_type=fav_type)
        if exist_records:
            '''记录存在，取消收藏'''
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_nums -= 1
                course_org.save()
            else:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                teacher.save()
            return HttpResponse(json.dumps({'status': 'fail', "msg": "取消收藏"}), content_type='application/json')

        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.fav_id = int(fav_type)
                user_fav.fav_type = fav_type
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_nums += 1
                    course_org.save()
                else:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse(json.dumps({'status': 'success', "msg": "收藏成功"}), content_type='application/json')

            else:
                return HttpResponse(json.dumps({'status': 'fail', "msg": "收藏出错"}), content_type='application/json')


class TeacherListView(View):
    '''课程讲师列表页'''

    def get(self, request):
        teachers = Teacher.objects.all()
        sort = request.GET.get("sort", "")
        order_teacher = Teacher.objects.all().order_by("-click_nums")[:5]
        keywords = request.GET.get('keywords', '')
        if keywords:
            '''课程讲师搜索'''
            # Q(work_company__icontains=keywords) or or Q(work_position__icontains=keywords)
            teachers = teachers.filter(Q(name__icontains=keywords))
        if sort == "hot":
            teachers = teachers.order_by("-click_nums")
        try:
            '''分页'''
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teachers, 3, request=request)
        current_nav = "teacher"
        teacher = p.page(page)
        return render(request, 'html/teachers-list.html', {"teachers": teacher,
                                                           'order_teacher': order_teacher,
                                                           "sort": sort,
                                                           'current_nav': current_nav, })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.click_nums += 1
        teacher.save()
        teacehr_course = teacher.course_set.all()
        order_teacher = Teacher.objects.all().order_by("-click_nums")[:5]
        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
            has_teacher_faved = True
        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
            has_org_faved = True
        return render(request, 'html/teacher-detail.html', {'teacher': teacher,
                                                            'teacehr_course': teacehr_course,
                                                            'order_teacher': order_teacher,
                                                            'has_teacher_faved': has_teacher_faved,
                                                            'has_org_faved': has_org_faved,
                                                            })
