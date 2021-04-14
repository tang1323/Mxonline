from django.shortcuts import render
from django.views.generic import View
from apps.operations.forms import UserFavForm, CommentsForm
from apps.operations.models import UserFavorite, CourseComments

# 前端会返回一个jsonResponse
from django.http import JsonResponse
from apps.courses.models import Course
from apps.organizations.models import CourseOrg, Teacher
from apps.operations.models import Banner


# 首页index.html在这里写
class IndexView(View):
    def get(self, request, *args, **kwargs):

        # 这个是实例化，取出全部，Banner定义了index，这里做一个升序的排序
        # 这是首页最大的那个轮播图片
        banners = Banner.objects.all().order_by("index")[0:4]

        # 取出所有的课程,是否是轮播图片还是课程, 这里取是网站内的课程，取6个数据。因为只有6个
        # 这是课程的轮播图片
        courses = Course.objects.filter(is_banner=False)[:6]

        # 取出轮播图片， 这个是轮播课程的图片
        banner_courses = Course.objects.filter(is_banner=True)

        # 取出课程机构轮播图片
        course_orgs = CourseOrg.objects.all()[:15]

        return render(request, "index.html", {
            "banners": banners,
            "courses": courses,
            "banner_courses": banner_courses,
            "course_orgs": course_orgs,
        })


# 用户章节里面的评论操作
class CommentView(View):
    # 从服务器推过去数据
    def post(self, request, *args, **kwargs):
        """
        用户收藏，用户取消收藏
        """
        # 要收藏先看看用户是否己经登录，用is_authenticated判断用户是否登录
        # 用JsonResponse来接收前端的数据，这个在org_base中的ajax
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"

            })
        # 如果没有己经登录，那就可以进行表单验证
        # 进行表单验证, 实例化
        comment_form = CommentsForm(request.POST)

        # 用is_valid的值做一个表单验证
        if comment_form.is_valid():

            # 收藏的实体id是多少,从服务器拿出来， 这个要和前端协商了
            # "course_id"是course-comment.html中的ajax
            course = comment_form.cleaned_data["course"]
            comments = comment_form.cleaned_data["comments"]

            # 请求用户相关信息
            comment = CourseComments()
            comment.user = request.user
            comment.comments = comments
            # 在CommentsForm里己经把在models定义的course拿过来了，是一个对象，已经是一个值，所以就不用取course_id了
            # course = Course.objects.get(id=course_id)
            comment.course = course
            comment.save()

            return JsonResponse({
                "status": "success",
            })
        # 不管是JsonResponse或者是render再或者是一个if分支，都要返回一个return
        # 这里是检测到is_valid是没有通过的话，如果不做这个else, 那就会抛一个异常,为严谨，要做一个else
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })


# 用户的收藏与用户取消收藏
class AddFavView(View):
    # 从服务器推过去数据
    def post(self, request, *args, **kwargs):
        """
        用户收藏，用户取消收藏
        """
        # 要收藏先看看用户是否己经登录，用is_authenticated判断用户是否登录
        # 用JsonResponse来接收前端的数据，这个在org_base中的ajax
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"

            })
        # 如果没有己经登录，那就可以进行表单验证
        # 进行表单验证, 实例化
        user_fav_form = UserFavForm(request.POST)

        # 用is_valid的值做一个表单验证
        if user_fav_form.is_valid():

            # 收藏的实体id是多少,从服务器拿出来， 这个要和前端协商了
            # "fav_id"是org_base中的ajax，如果没有fav_id，那默认是0
            fav_id = user_fav_form.cleaned_data["fav_id"]
            fav_type = user_fav_form.cleaned_data["fav_type"]

            # 取出来后判断一下用户是否己经收藏过
            # 查询一下数据库, 用filter是过滤器的意思
            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)

            # 如果取到收藏记录己经存在，再次点击就是取消收藏
            if existed_records:
                existed_records.delete()

                # 因为有几种收藏类型，比如课程或者老师，如果己经等于1
                # fav_nums在UserFavorite的models我们都定义了这个字段
                # (1, "课程"), (2, "课程机构"), (3, "讲师"),在UserFavorite里定义了
                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums -= 1
                    course_org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()

                # 不管是收藏或者是取消收藏都是返回一个点击后的内容
                return JsonResponse({
                    "status": "success",
                    "msg": "收藏"

                })

            # 如果收藏，那就添加一个收藏
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "己收藏"

                })
        # 不管是JsonResponse或者是render再或者是一个if分支，都要返回一个return
        # 这里是检测到is_valid是没有通过的话，如果不做这个else, 那就会抛一个异常,为严谨，要做一个else
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })



























