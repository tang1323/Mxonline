from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Q # 搜索用的


from apps.organizations.models import CourseOrg
from apps.organizations.models import City, Teacher
from apps.organizations.forms import AddAskForm
from apps.operations.models import UserFavorite


# 讲师详情页面
class TeacherDetailView(View):
    def get(self, request, teacher_id, *args, **kwargs):
        # 得到全部teacher 的id
        teacher = Teacher.objects.get(id=int(teacher_id))

        # 老师的收藏状态
        teacher_fav = False

        # 课程的收藏状态
        org_fav = False

        # 获取是否登录
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                teacher_fav = True

            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                org_fav = True

        # 这是讲师排行榜
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "teacher_fav": teacher_fav,
            "org_fav": org_fav,
            "hot_teachers": hot_teachers,
        })


# 讲师列表页的view
class TeacherListView(View):
    def get(self, request, *args, **kwargs):
        # 从数据库中获取数据, 从models取出数据来

        # 把数据全部取出来,查询
        all_teachers = Teacher.objects.all()

        # 有几个讲师
        teacher_nums = all_teachers.count()

        # 这是讲师排行榜
        hot_teachers = Teacher.objects.all().order_by("-click_nums")[:3]

        # 搜索关键词, keywords要和前端的keywords保持一致， 默认空字符串
        keywords = request.GET.get("keywords", "")

        # 搜索时候的状态是否选中
        s_type = "teacher"

        # 如果两者一样
        if keywords:
            # 进一步过滤，因为course有好几个，这里可以搜索name，字段
            # name__icontains有i是忽略大小写的，
            # 我们要的是在任何字段出现的都可以被搜索出来，那我们就用到了Q, 这里只搜索两个字段
            all_teachers = all_teachers.filter(Q(name__icontains=keywords))

        # 对讲师人气进行排序
        # 从get里面获取
        sort = request.GET.get("sort", "")
        if sort == "hot":
            # 对人气进行排序，加了-，就是从大到小
            all_teachers = all_teachers.order_by("-click_nums")

        # 对讲师在进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # per_page=5，每页有几条数据,,orgs：就是分页之后的对象，所以render要显示在前端
        p = Paginator(all_teachers, per_page=3, request=request)
        teachers = p.page(page)

        return render(request, "teachers-list.html", {
            "teachers": teachers,
            "teacher_nums": teacher_nums,
            "sort": sort,
            "hot_teachers": hot_teachers,
            "keywords": keywords,
            "s_type": s_type,

        })


# 授课机构下的课程机构中的机构介绍
class OrgDescView(View):
    def get(self, request, org_id, *args, **kwargs):
        # 设置这个变量,如果是点击选中状态,那就是这个变量
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 这是授课机构上边大家共用的一个授课机构的收藏
        has_fav_org = False
        if request.user.is_authenticated:
            """
            requests还未登录的时候也是可以取，但是是一个内部的一个类,是一个匿名的类
            所以一开始做一个is_authenticated就能保证我们request回来是一个userprofile对象
            """
        # fav_type=2在UserFavorite定义了是一个课程机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav_org = True

        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav_org": has_fav_org,
        })


# 授课机构下的课程机构中的机构课程
class OrgCourseView(View):
    def get(self, request, org_id, *args, **kwargs):
        # 设置这个变量,如果是点击选中状态,那就是这个变量
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 这是授课机构上边大家共用的一个授课机构的收藏
        has_fav_org = False
        if request.user.is_authenticated:
            """
            requests还未登录的时候也是可以取，但是是一个内部的一个类,是一个匿名的类
            所以一开始做一个is_authenticated就能保证我们request回来是一个userprofile对象
            """
        # fav_type=2在UserFavorite定义了是一个课程机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav_org = True

        # 不做切片,本身要显示所有的course
        all_courses = course_org.course_set.all()

        # 对课程机构在进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # per_page=5，每页有几条数据,,orgs：就是分页之后的对象，所以render要显示在前端
        p = Paginator(all_courses, per_page=3, request=request)
        courses = p.page(page)

        return render(request, "org-detail-course.html", {
            # 这里做了分页,所以是courses
            "all_courses": courses,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav_org": has_fav_org,
        })


# 授课机构下的课程机构中的机构讲师
class OrgTeacherView(View):
    def get(self, request, org_id, *args, **kwargs):
        # 设置这个变量,如果是点击选中状态,那就是这个变量
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_nums += 1
        course_org.save()

        # 这是授课机构上边大家共用的一个授课机构的收藏
        has_fav_org = False
        if request.user.is_authenticated:
            """
            requests还未登录的时候也是可以取，但是是一个内部的一个类,是一个匿名的类
            所以一开始做一个is_authenticated就能保证我们request回来是一个userprofile对象
            """
        # fav_type=2在UserFavorite定义了是一个课程机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav_org = True

        # 不做切片,本身要显示所有的teacher
        all_teacher = course_org.teacher_set.all()

        return render(request, "org-detail-teachers.html", {
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav_org": has_fav_org,
        })


# 授课机构下的课程机构中的机构首页的详情页面
class OrgHomeView(View):
    def get(self, request, org_id, *args, **kwargs):

        # 设置这个变量,如果是点击选中状态,那就是这个变量
        current_page = "home"

        # 从后台取出数据,先处理下org_id
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 谁点进来就做一个保存
        course_org.click_nums += 1
        course_org.save()

        # 这是授课机构上边大家共用的一个授课机构的收藏
        has_fav_org = False
        if request.user.is_authenticated:
            """
            requests还未登录的时候也是可以取，但是是一个内部的一个类,是一个匿名的类
            所以一开始做一个is_authenticated就能保证我们request回来是一个userprofile对象
            """
        # fav_type=2在UserFavorite定义了是一个课程机构
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav_org = True

        # 从后台courses模块和organizations模块取出数据,这里课程只取3个,切片
        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]

        return render(request, "org-detail-homepage.html", {
            "all_courses": all_courses,
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav_org": has_fav_org,
        })


# 用户咨询的提交
class AddAskView(View):
    """
    处理用户的咨询
    """
    # 只是用户提交信息而已，不会从服务上拉数据下来。所以用重载post方法就行了
    def post(self, request, *args, **kwargs):
        # userask_form继承的是AddAskForm的实例
        userask_form = AddAskForm(request.POST)

        # 验证表单这个is_valid值是否有问题
        if userask_form.is_valid():
            # commit=True设置了之后才交给数据库执行，不然save只是提交给数据库而已
            userask_form.save(commit=True)

            # 返回json
            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "添加出错",
            })


# 机构相关页面
class OrgView(View):
    def get(self, request, *args, **kwargs):
        # 从数据库中获取数据, 从models取出数据来

        # 把数据全部取出来
        all_orgs = CourseOrg.objects.all()

        # 有几家, 不能在这里统计，不然是一个总数
        # org_nums = CourseOrg.objects.count()

        # 从后台数据库读取有哪些城市,读出所有数据objects.all()
        all_citys = City.objects.all()

        # 授课机构的排名，点击筛选了之后要做一个全量的数据进行排名，所以要写在这里
        hot_orgs = all_orgs.order_by("-click_nums")[:3]


        # 搜索关键词, keywords要和前端的keywords保持一致， 默认空字符串
        keywords = request.GET.get("keywords", "")
        # 搜索时候的状态是否选中
        s_type = "org"
        # 如果两者一样
        if keywords:
            # 进一步过滤，因为course有好几个，这里可以搜索name，desc,字段
            # name__icontains有i是忽略大小写的，
            # 我们要的是在任何字段出现的都可以被搜索出来，那我们就用到了Q, 这里只搜索两个字段
            all_orgs = all_orgs.filter(Q(name__icontains=keywords) | Q(desc__icontains=keywords))

        # 通过机构类别对课程机构进行筛选, ct跟前端要保持一致, ""是默认值，是空的意思
        category = request.GET.get("ct", "")
        if category:
            # category要跟CourseOrg里的字段保持一致
            all_orgs = all_orgs.filter(category=category)

        # 通过所在城市对课程机构进行筛选, city_id在数据库有，不要用city来取，不然也是要从city里取city_id，这样会多一层查询
        city_id = request.GET.get("city", "")
        if city_id:
            # isdigit能判断是否是不是数字类型的
            if city_id.isdigit():
                all_orgs = all_orgs.filter(city_id=int(city_id))

        # 对机构进行排序
        # 从get里面获取
        sort = request.GET.get("sort", "")
        if sort == "students":
            # 对学习人数进行排序。在CourseOrg定义了，加了-，就是从大到小
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            # 对学习人数进行排序。在CourseOrg定义了，加了-，就是从大到小,也要跟前端保持一致
            all_orgs = all_orgs.order_by("-course_nums")






        # 有几家课程
        org_nums = all_orgs.count()
        # 对课程机构在进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # per_page=5，每页有几条数据,,orgs：就是分页之后的对象，所以render要显示在前端
        p = Paginator(all_orgs, per_page=3, request=request)
        orgs = p.page(page)



        # 展示到页面
        return render(request, "org-list.html", {
            "all_orgs": orgs,
            "org_nums": org_nums,
            "all_citys": all_citys,
            "category": category,
            "city_id": city_id,
            "sort": sort,
            "hot_orgs": hot_orgs,
            "keywords": keywords,

        })

















