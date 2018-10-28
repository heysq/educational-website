from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
from .models import Course
from pure_pagination import EmptyPage, PageNotAnInteger, Paginator
from operation.models import UserFavorite, CourseComment, UserCourse
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q
import  json
class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by("-add_time")
        hot_course = all_courses.order_by("fav_nums")[0:2]
        sort = request.GET.get('sort', "default")
        current_nav = "course"
        keywords = request.GET.get('keywords','')
        if keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=keywords)or
                Q(desc__icontains=keywords)or
                Q(detail__icontains=keywords))

        if sort == "default":
            all_courses = all_courses
        elif sort == "students":
            all_courses = all_courses.order_by("-students")
        else:
            all_courses = all_courses.order_by('-click_nums')
        try:
            '''分页'''
            page = request.GET.get("page", 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)
        return render(request, 'html/course-list.html',
                      {"all_courses": courses,
                       'hot_course': hot_course,
                       'sort': sort,
                       'current_nav':current_nav})


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.click_nums +=1
        course.save()
        tag = course.tag
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True
        if tag:
            relate_course = Course.objects.filter(tag=tag)[0]
        else:
            relate_course = Course.objects.order_by('-add_time')[0]
        return render(request, 'html/course-detail.html', {'course': course,
                                                           'relate_course': relate_course,
                                                           'has_fav_course': has_fav_course,
                                                           'has_fav_org': has_fav_org,
                                                           })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course.students += 1
        course.save()
        '''课程与用户进行关联'''
        user_courses = UserCourse.objects.filter(user=request.user,course=course,)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)

            user_course.save()
        user_ids = [user_course.user.id for user_course in user_courses]
        '''django 黑魔法  两个下划线实现 实现列表遍历'''
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        youneed_konw =course.youneed_know
        teacher_tell = course.teahcher_tell
        '''所有课程id'''
        relate_ids = [user_course.course.id for user_course in all_user_courses]
        courses = Course.objects.filter(id__in=relate_ids).order_by('-click_nums')[:3]
        return render(request, 'html/course-video.html', {
            'course': course,
            'courses': courses,
            'youneed_konw':youneed_konw,
            'teacher_tell':teacher_tell,
        })


class CommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=course_id)
        all_comments = CourseComment.objects.all()
        return render(request, 'html/course-comment.html', {
            'course': course,
            'all_comments': all_comments,
        })


class AddCommentView(View):
    '''用户添加课程评论'''

    def post(self, request):
        if not request.user.is_authenticated():
            '''未登录'''
            res = {'status': 'fail', "msg": "用户为登录"}
            return HttpResponse(json.dumps(res), content_type='application/json')
        course_id = request.POST.get('course_id', '')
        comments = request.POST.get('comments', '')
        if int(course_id) > 0 and comments:
            course_comment = CourseComment()
            course = Course.objects.get(id=int(course_id))
            course.id = int(course_id)
            course_comment.course = course
            course_comment.comments = comments
            course_comment.user = request.user
            course_comment.save()
            res = {'status': 'success', "msg": "添加成功"}
            return HttpResponse(json.dumps(res), content_type='application/json')
        else:
            res = {'status': 'fail', "msg": "添加失败"}
            return HttpResponse(json.dumps(res), content_type='application/json')
