from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q # 搜索用的


from apps.courses.models import Course, CourseTag, CourseResource, Video
from apps.operations.models import UserFavorite, UserCourse, CourseComments


class VideoView(LoginRequiredMixin, View):
    # 己经引进LoginRequiredMixin，如果没有登录，则会跳转到登录页面
    login_url = "/login/"

    def get(self, request, course_id, video_id,  *args, **kwargs):
        """
        获取视频信息
        """
        # 获取一下course_id
        course = Course.objects.get(id=int(course_id))
        # 点击数加1及保存
        course.click_nums += 1
        course.save()

        video = Video.objects.get(id=int(video_id))

        # 查询用户是否已经关联了该课程
        # 如果进入这个逻辑，那就是一个登录的状态了
        user_courses = UserCourse.objects.filter(user=request.user, course=course)

        # 如果没有这个记录的话，那就生成这个记录
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        # 学过该课程的所有同学id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取所有同学的所有课程, 点击数的倒序排列
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]

        # 相关课程, 列表生成式可读性不是很好
        # related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        related_courses = []
        for item in all_courses:
            # 对当前课程进行过滤，以免推荐相同的课程， 不能等于当前的course.id
            if item.course.id != course.id:
                related_courses.append(item.course)

        # 课程资源的下载
        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-play.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "video": video,
        })


# 课程评论
class CourseCommentsView(LoginRequiredMixin, View):
    # 己经引进LoginRequiredMixin，如果没有登录，则会跳转到登录页面
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        # 获取一下course_id
        course = Course.objects.get(id=int(course_id))
        # 点击数加1及保存
        course.click_nums += 1
        course.save()

        # 查询评论
        comments = CourseComments.objects.filter(course=course)

        # 查询用户是否已经关联了该课程
        # 如果进入这个逻辑，那就是一个登录的状态了
        user_courses = UserCourse.objects.filter(user=request.user, course=course)

        # 如果没有这个记录的话，那就生成这个记录
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        # 学过该课程的所有同学id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取所有同学的所有课程, 点击数的倒序排列
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]

        # 相关课程, 列表生成式可读性不是很好
        # related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        related_courses = []
        for item in all_courses:
            # 对当前课程进行过滤，以免推荐相同的课程， 不能等于当前的course.id
            if item.course.id != course.id:
                related_courses.append(item.course)

        # 课程资源的下载
        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "comments": comments,
        })


# 课程章节信息
class CourseLessonView(LoginRequiredMixin, View):
    # 己经引进LoginRequiredMixin，如果没有登录，则会跳转到登录页面
    login_url = "/login/"

    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程章节信息
        """
        # 获取一下course_id
        course = Course.objects.get(id=int(course_id))
        # 点击数加1及保存
        course.click_nums += 1
        course.save()

        # 1. 用户和课程之间的关联
        # 2. 对view进行login登录的验证
        # 3.其他课程

        # 查询用户是否已经关联了该课程
        # 如果进入这个逻辑，那就是一个登录的状态了
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        # 如果没有这个记录的话，那就生成这个记录
        if not user_courses:
            user_courses = UserCourse(user=request.user, course=course)
            user_courses.save()
            course.students += 1
            course.save()

        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        # 学过该课程的所有同学id
        user_ids = [user_course.user.id for user_course in user_courses]
        # 取所有同学的所有课程, 点击数的倒序排列
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]

        # 相关课程, 列表生成式可读性不是很好
        # related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]
        related_courses = []
        for item in all_courses:
            # 对当前课程进行过滤，以免推荐相同的课程， 不能等于当前的course.id
            if item.course.id != course.id:
                related_courses.append(item.course)

        # 课程资源的下载
        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-video.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
        })


# 公开课课程里面的详情页面
class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        """
        获取课程详情
        """
        # 获取一下course_id
        course = Course.objects.get(id=int(course_id))
        # 点击数加1及保存
        course.click_nums += 1
        course.save()

        # 获取收藏状态
        # 因为这里有两个收藏的按钮
        # 这是课程详情页面的一个收藏
        has_fav_course = False

        # 这是右边的一个授课机构的收藏
        has_fav_org = False
        if request.user.is_authenticated:
            """
            requests还未登录的时候也是可以取，但是是一个内部的一个类,是一个匿名的类
            所以一开始做一个is_authenticated就能保证我们request回来是一个userprofile对象
            """
            # fav_type=1在UserFavorite定义了是一个课程类型
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            # fav_type=2在UserFavorite定义了是一个课程机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 通过课程的tag做课程的推荐
        # 一个课程要有多个tag(课程标签)，所以要添加一个models
        # tag = course.tag
        # related_courses = []
        # if tag:
        #     # exclude(id=course.id)是排除当前的id，这样就不会推荐当前的课程
        #     # id__in=[course.id],是过滤一批数据
        #     related_courses = Course.objects.filter(tag=tag).exclude(id__in=[course.id])[:3]

        """
        这个是外键反取，coursetag_set是怎么来呢，分两部分，
        1.coursetag是CourseTag方法的一个小写，也是调用这个CourseTag方法
        2.那_set是怎么出现的呢，如果我们这个方法CourseOrg是Course的一个外键，那么就可以反向取，
        所以加起来就是coursetag_set
        """
        # 取出所有的标签
        tags = course.coursetag_set.all()
        # 循环tag下的tag字段
        tag_list = [tag.tag for tag in tags]

        # exclude(id=course.id)是排除当前的id，这样就不会推荐当前的课程
        # id__in=[course.id],是过滤一批数据
        # course__id双下划线是取course的id属性，course_id单下划线是取course的属性，都是可以，但是双下划线用处非常多，只有id才能双下划线
        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)

        # set()是去重的方法，是不允许有相同的值
        related_courses = set()
        # 这里直接取CourseTag下的course, 这样我们就有取到相关的课程名称了
        for course_tag in course_tags:
            # 配合set()用add()，不能再用append方法了
            related_courses.add(course_tag.course)

        return render(request, "course-detail.html", {
            "course": course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            "related_courses": related_courses,
        })


# 公开课的列表
class CourseListView(View):
    # 这是一个对数据库一个拉的过程，用get就行
    def get(self, request, *args, **kwargs):
        """
        获取课程列表信息
        """

        # 获取所有的课程就用all()
        # 因为要做一个排序，所有用order_by,,,-add_time是一个倒序, 就是最新的课程
        all_courses = Course.objects.order_by("-add_time")

        # 热门推荐与最热门的一样
        hot_course = Course.objects.order_by("-click_nums")[:3]

        # 搜索关键词, keywords要和前端的keywords保持一致， 默认空字符串
        keywords = request.GET.get("keywords", "")
        # 搜索时候的状态是否选中
        s_type = "course"
        # 如果两者一样
        if keywords:
            # 进一步过滤，因为course有好几个，这里可以搜索name，desc, detail字段
            # name__icontains有i是忽略大小写的，
            # 我们要的是在任何字段出现的都可以被搜索出来，那我们就用到了Q
            all_courses = all_courses.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(detail__icontains=keywords))


        # 课程排序
        # 找到前端排序的字段，在course-list里面在最新的排序下就有一个叫sort，这个要和后端保持一致
        # 在url的参数都放在GET中，而不是放在post里面
        # ("sort", ""), 如果没有找到的话要取空值
        sort = request.GET.get("sort", "")
        # 如果等于前端的一个students， 那就做这个students的排序
        if sort == "students":
            # 这里的students是在models的下的，做一个倒序的排列
            all_courses = all_courses.order_by("-students")

        # 如果等于前端的一个hot， 那就做这个hot的排序
        elif sort == "hot":
            # 这里的click_nums是在models的下的，做一个倒序的排列
            all_courses = all_courses.order_by("-click_nums")

        # 对课程机构在进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # per_page=5，每页有几条数据,,orgs：就是分页之后的对象，所以render要显示在前端
        p = Paginator(all_courses, per_page=6, request=request)
        courses = p.page(page)

        return render(request, "course-list.html", {
            "all_courses": courses,
            "sort": sort,
            "hot_course": hot_course,
            "keywords": keywords,
            "s_type": s_type,
        })














