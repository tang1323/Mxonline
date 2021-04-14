from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout     # 通过authenticate就能判断帐号和密码是否正确
from django.http import HttpResponseRedirect, JsonResponse  # 登录成功之后要返回首页的一个网址, JsonResponse是可以返回我们的前端js，的js数据
from django.urls import reverse     # 可以跟login配置url页面一样，容易定位url是什么，后期维护性好
import redis
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.backends import ModelBackend   # 自定义身份验证
from django.db.models import Q      # 查询字段是否存在


from pure_pagination import Paginator, PageNotAnInteger
from apps.utils.YunPian import send_single_sms  # 手机验证码的发送
from Mxonline.settings import yp_apikey, REDIS_HOST, REDIS_PORT     # 云片网的apikey
from apps.utils.random_str import generate_random   # 随机生成字符串给手机发送验证码的
from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, UploadImageForm
from apps.users.forms import UserInfoForm, ChangePwdForm
from apps.users.forms import RegisterGetForm, RegisterPostForm, UpdateMobileForm
from apps.users.models import UserProfile
from apps.operations.models import UserFavorite, UserMessage, Banner
from apps.organizations.models import CourseOrg, Teacher
from apps.courses.models import Course

# 1.使用CBV(class base view)


# 自定义身份验证
# 这个方法要配置到settings当中
# AUTHENTICATION_BACKENDS = [
#     "apps.users.views.CustomAuth"
# ]
class CustomAuth(ModelBackend):
    # 重载这个方法
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 用Q来查询username是否等于username和mobile, 不管输对了username或者是mobile，都能登录
            # 在这里能用username或者mobile都能登录
            user = UserProfile.objects.get(Q(username=username)|Q(mobile=username))
            # 将这个用记的明文的密码传进来， 但它也会和数据库一样进行加密
            if user.check_password(password):
                # 必须返回一个user，因为我们在LoginView()说了必须得到这个user
                return user
        # 如果查询不到
        except Exception as e:
            # 那就返回一个none
            return None


# 这是一个全局的一个变量,就是未读消息,这样就不用为每个base页面写相同的逻辑了
# 这是在settings里的一个'django.template.context_processors.media',中的第一个方法,我们可以像它那样定义
# 这个写好了之后就配置到settings中TEMPLATES
def message_nums(request):
    """
    Add media-related context variables to the context.
    """
    # 判断是否已经登录,如果己经登录,那就放一个全局的变量
    if request.user.is_authenticated:
        return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
    # 如果没有登录,那就返回一个空字典
    else:
        return {}


# 个人中心下的我的消息
class MyMessageView(LoginRequiredMixin, View):
    # 己经引进LoginRequiredMixin，如果没有登录，则会跳转到登录页面
    login_url = "/login/"

    def get(self, request, *args, **kwargs):

        # 在operations下的models中有个UserMessage做用户消息的
        messages = UserMessage.objects.filter(user=request.user)

        # 选中的状态定义
        current_page = "message"

        # 这个是遍历未读的消息,你一进来就将has_read = True就变成己读的了
        for message in messages:
            message.has_read = True
            message.save()

        # 对我的消息在进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # per_page=5，每页有几条数据,,orgs：就是分页之后的对象，所以render要显示在前端
        p = Paginator(messages, per_page=3, request=request)
        messages = p.page(page)

        return render(request, "usercenter-message.html", {
            "messages": messages,
            "current_page": current_page,
        })


# 在个人中心的我的收藏下的公开课程
class MyFavCourseView(LoginRequiredMixin, View):
    # 己经引进LoginRequiredMixin，如果没有登录，则会跳转到登录页面
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        # 选中的状态定义
        current_page = "myfav_course"

        # 做一个查询,要给前端返回全部的课程机构
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)

        for fav_course in fav_courses:
            # 查询公开课程, course是一个实例化
            # 这个个try是如果在数据库的courses_course中的id没有了从1开始,那就做一个try
            try:
                course = Course.objects.get(id=fav_course.fav_id)
                course_list.append(course)
            # 如果有异常那就证明是被删掉了
            except Course.DoesNotExist as e:
                pass

        return render(request, "usercenter-fav-course.html", {
            "course_list": course_list,
            "current_page": current_page,
        })


# 在个人中心的我的收藏下的授课老师
class MyFavTeacherView(LoginRequiredMixin, View):
    # 己经引进LoginRequiredMixin，如果没有登录，则会跳转到登录页面
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        # 选中的状态定义
        current_page = "myfav_teacher"

        # 做一个查询,要给前端返回全部的课程机构
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)

        for fav_teacher in fav_teachers:
            # 查询授课教师, teacher是一个实例化
            teacher = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(teacher)

        return render(request, "usercenter-fav-teacher.html", {
            "teacher_list": teacher_list,
            "current_page": current_page,
        })


# 在个人中心的我的收藏下的课程机构
class MyFavOrgView(LoginRequiredMixin, View):
    # 己经引进LoginRequiredMixin，如果没有登录，则会跳转到登录页面
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        # 选中的状态定义
        current_page = "myfavorg"

        # 做一个查询,要给前端返回全部的课程机构
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)

        for fav_org in fav_orgs:
            # 查询课程机构, org是一个实例化
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)

        return render(request, "usercenter-fav-org.html", {
            "org_list": org_list,
            "current_page": current_page,
        })


# 个人资料的我的课程
# 重点:如果这个view太过简单,那能在urls里面能直接配置个一个TemplateView也行,具体看urls,所以可以注释掉
# class MyCourseView(LoginRequiredMixin, View):
#     # 己经引进LoginRequiredMixin，如果没有登录，则会跳转到登录页面
#     login_url = "/login/"
#
#     def get(self, request, *args, **kwargs):
#         # 选中的状态定义
#         current_page = "mycourse"
#
#         # 查询到返回给前端html循环一个课程
#         # 如果外键反向取就不用这句话,在usercenter-mycourse.html的39行说明
#         # my_courses = UserCourse.objects.filter(user=request.user)
#         return render(request, "usercenter-mycourse.html", {
#             # "my_courses": my_courses,
#             "current_page": current_page,
#         })


# 修改手机的号码的一个view
class ChangeMobileView(LoginRequiredMixin, View):
    # 己经引进LoginRequiredMixin，如果没有登录，则会跳转到登录页面
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        # 从数据库取值时先forms表单验证
        mobile_form = UpdateMobileForm(request.POST)

        # 判断值对不对
        if mobile_form.is_valid():
            # 这是新的手机号码
            mobile = mobile_form.cleaned_data["mobile"]

            # 如果和当前的号码一致
            # if request.user.mobile == mobile:
            #     return JsonResponse({
            #         "mobile": "和当前号码一致"
            #     })

            # 已经存在的记录不能重复注册，就是这个手机号码已经注册在数据库就不能再注册
            if UserProfile.objects.filter(mobile=mobile):
                # 如果己经注册过，那就返回一个错误信息
                return JsonResponse({
                    "mobile": "该手机号码已经被占用 "
                })

            # 如果不一致，那就保存到数据库
            user = request.user
            user.mobile = mobile
            # 修改手机号码后的username也等于mobile,登录的时候是根据username来登录的
            user.username = mobile
            user.save()
            return JsonResponse({
                "status": "success"
            })
        # 如果表单验证失败的话,那就返回一个错误
        else:
            return JsonResponse(mobile_form.errors)

            # 修改密码后要不要退出,要不要继续登录？就根据自己的需求决定
            # logout(request, user)
            # login(request, user)


# 在个人中心修改密码的view
class ChangePwdView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        # 从form传过来的方法实例化
        pwd_form = ChangePwdForm(request.POST)

        # 看看值对不对
        if pwd_form.is_valid():

            # 没有password1则为空字符
            # pwd1是新密码，pwd2是确认密码
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")

            # 这个己经给forms表单做了
            # if pwd1 != pwd2:
            #     return JsonResponse({
            #         "status": "fail",
            #         "msg": "密码不一致",
            #     })

            # 如果新密码和确认密码没有问题的话
            user = request.user
            user.set_password(pwd1)
            user.save()

            # 修改密码后,django会自动帮我们退出，是很合理，那也有不让它退出的
            # 这个就根据自己的业务逻辑需求要不要
            # login(request, user)

            return JsonResponse({
                "status": "success"
            })
        # 如果在form表单验证失败的话，就执行这个,返回一个在前端定义的一个错误
        else:
            return JsonResponse(pwd_form.errors)


# 读取图片，是一个头像，然后对图片保存
class UploadImageView(LoginRequiredMixin, View):
    # 己经引进LoginRequiredMixin，如果没有登录，则会跳转到登录页面
    login_url = "/login/"

    # 接收一个文件做一个保存，是一个内部的一个方法
    # def save_file(self, file):
    #     with open("D:/Py-Project/Mxonline/media/head_image/uploaded.jpg", "wb") as f:
    #         # 就要用chunks这个方法
    #         for chunk in file.chunks():
    #             f.write(chunk)

    # 是向数据库更换一个图片，就是推
    def post(self, request, *args, **kwargs):
        # 处理用户上传的头像, 一定要用FILES这个
        # 实例化一下这个传过来的方法
        # POST只存放非文件的数据，所以我们需要FILES, 如果不写这个instance=request.user，那UploadImageForm会以为是一个新的数据，所以一定一定要记得写
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        # is_valid值是否存在
        if image_form.is_valid():
            image_form.save()
            # 成功保存就返回 一个JsonResponse
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })

        # 这个方法不推荐，因为下面的三个问题需要一一解决，但用modelform就能很好的解决
        # files = request.FILES["image"]
        # self.save_file(files)

        # 1.如果同一个文件上传多次， 相同名称的文件应该如何处理
        # 2.文件的保存路径应该写入到user下的models的UserProfile的image
        # 3.还没有做表单验证
        # 重点：：：：：：：用modelform就能完成上面的3个问题


# 个人中心的头像修改，用户的信息修改， 与手机号码的修改(需要图片验证码RegisterGetForm)
class UserInfoView(LoginRequiredMixin, View):
    # 己经引进LoginRequiredMixin，如果没有登录，则会跳转到登录页面
    login_url = "/login/"

    # 这是拉
    def get(self, request, *args, **kwargs):
        # 选中的状态定义
        current_page = "info"

        # 这是修改手机号码的图片验证码
        captcha_form = RegisterGetForm()
        return render(request, "usercenter-info.html", {
            "captcha_form": captcha_form,
            "current_page": current_page,
        })

    # 这是推给数据库，因为要向数据库修改数据，所以用个post
    def post(self, request, *args, **kwargs):
        # 做一个实例化
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            # 成功保存就返回 一个JsonResponse
            return JsonResponse({
                "status": "success"
            })

        else:
            # 这个在前端的jsEditUserBtn已经定义要好返回错误的字段，这里做一个显示就行了
            return JsonResponse(user_info_form.error)


# 这是注册的页面
class RegisterView(View):
    # 图片验证码返回前端
    def get(self, request, *args, **kwargs):
        register_get_form = RegisterGetForm()

        # 首页的轮播图片
        banners = Banner.objects.all()[4:7]
        return render(request, "register.html", {
            "register_get_form": register_get_form,
            "banners": banners,
        })

    def post(self, request, *args, **kwargs):

        # 拿去校验
        register_post_form = RegisterPostForm(request.POST)

        # 首页的轮播图片
        banners = Banner.objects.all()[4:7]

        # 用is_valid这个值来判断一下
        if register_post_form.is_valid():
            # 没有注册帐号依然可以登录
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]

            # 如果用户不存在，新建一个用户
            user = UserProfile(username=mobile)
            user.set_password(password)
            user.mobile = mobile
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            # 再传一个图片验证码进来
            register_get_form = RegisterGetForm()
            # 如果用户名密码错误，则返回error给用户，是哪个字段没有填，会出红色框框
            return render(request, "register.html", {
                "register_get_form": register_get_form,
                "register_post_form": register_post_form,
                "banners": banners,
            })


# 实现动态手机验证码的登录的接口
class DynamicLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        # 这个是在没有登录的时候要进入章节课程时，登录之后自动跳转到课程章节下，因为登录时候有个next，后面接着该章节的url
        # 这是一个用get方法才能请求的到。所以放在这里
        next = request.GET.get("next", "")

        login_form = DynamicLoginView()

        # 首页的轮播图片
        banners = Banner.objects.all()[4:7]
        return render(request, "login.html", {
            "login_form": login_form,
            "next": next,
            "banners": banners,

        })

    def post(self, request, *args, **kwargs):
        # 拿去校验
        login_form = DynamicLoginPostForm(request.POST)

        # 这个变量用来接收当前正在是手机动态页面登录的
        dynamic_login = True

        # 首页的轮播图片
        banners = Banner.objects.all()[4:7]

        # 用is_valid这个值来判断一下
        if login_form.is_valid():
            # 没有注册帐号依然可以登录
            mobile = login_form.cleaned_data["mobile"]

            # 去这个表看看有没有这个帐号， filter不抛异常，get是抛异常
            existed_users = UserProfile.objects.filter(mobile=mobile)
            # 如果用户存在
            if existed_users:
                user = existed_users[0]

            # 如果用户不存在，新建一个用户
            else:
                user = UserProfile(username=mobile)
                # 随机生成一个密码，用户都不知道
                password = generate_random(10, 2)
                user.set_password(password)
                user.mobile = mobile
                user.save()
            login(request, user)

            # 这个是在没有登录的时候要进入章节课程时，登录之后自动跳转到课程章节下，因为登录时候有个next，后面接着该章节的url
            # 这个在上面的get方法也要有定义，因为get方法才能获取得到它的一个url
            next = request.GET.get("next", "")
            if next:
                return HttpResponseRedirect(next)

            next = request.GET.get("next", "")
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse("index"))

        else:
            # 再传一个图片验证码进来
            d_form = DynamicLoginForm()
            # 如果用户名密码错误，则返回error给用户，是哪个字段没有填，会出红色框框
            return render(request, "login.html", {
                "login_form": login_form,
                "dynamic_login": dynamic_login,
                "d_form": d_form,
                "banners": banners,
            })


# 发送验证码和手机去提交验证
class SendSmsView(View):
    # 重载post这个方法
    def post(self, request, *args, **kwargs):

        # 动态验证码的一个forms，必须要有几个字段，第一个是图片验证码，第二个是手机号码
        send_sms_form = DynamicLoginForm(request.POST)

        # 接收返回错的字段
        re_dict = {}

        # 用is_valid这个值来判断一下
        if send_sms_form.is_valid():

            # 发送手机验证码
            mobile = send_sms_form.cleaned_data["mobile"]

            # 随机生成数字验证码
            code = generate_random(6, 0)

            # 给云片网发送给我们的手机
            re_json = send_single_sms(yp_apikey, code, mobile=mobile)

            # 返回等于0，验证成功,,, status这个要跟前前端商量好，要一致
            if re_json["code"] == 0:
                re_dict["status"] = "success"

                # 连接redis，让redis来存储随机验证码和计算过期时间
                r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
                r.set(mobile, code)# 设置手机和验证码
                r.expire(str(mobile), 60*5)# 设置验证码5分钟过期

            else:
                re_dict["msg"] = re_json["msg"]

        else:
            # 如果表单验证失败就会返回我们的一个errors
            for key, value in send_sms_form.errors.items():

                # 看一下是什么错了，拆包
                re_dict[key] = value[0]

        # 最终返回我们前端的一个js数据给浏览器
        return JsonResponse(re_dict)


# 退出接口
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


# 登录
class LoginView(View):
    def get(self, request, *args, **kwargs):

        # 判断用户是否登录, is_authenticated是一个属性
        if request.user.is_authenticated:
            # 跳转到首页
            return HttpResponseRedirect(reverse("index"))

        # 首页的轮播图片
        banners = Banner.objects.all()[4:7]

        # 这个是在没有登录的时候要进入章节课程时，登录之后自动跳转到课程章节下，因为登录时候有个next，后面接着该章节的url
        # 这是一个用get方法才能请求的到。所以放在这里
        # 这个要配置到login.html中第77行?next={{ next }}
        next = request.GET.get("next", "")

        # 图像验证码的实例
        login_form = DynamicLoginForm()

        return render(request, "login.html", {
            "login_form": login_form,
            "next": next,
            "banners": banners,
        })

    # 获取用户帐号和密码，表单验证
    def post(self, request, *args, **kwargs):
        # 用户前端提交过来的数据我们叫表单验证forms
        login_form = LoginForm(request.POST)

        # 首页的轮播图片
        banners = Banner.objects.all()[4:7]

        # 通过这个表单认证就可以继续后续的逻辑了
        if login_form.is_valid():

            # 定位登录帐号跟密码， cleaned_data提取且的值
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # 用于通过用户和密码查询用户是否存在
            # 验证帐号和密码是否正确,user是UserProfile(专门存帐号密码的一个数据库)一个对象，成功就返回一个user对象,否则null
            user = authenticate(username=user_name, password=password)


            # 做一个判断
            if user is not None:
                # 查询到用户
                login(request, user)

                # 这个是在没有登录的时候要进入章节课程时，登录之后自动跳转到课程章节下，因为登录时候有个next，后面接着该章节的url
                # 这个在上面的get方法也要有定义，因为get方法才能获取得到它的一个url
                next = request.GET.get("next", "")
                if next:
                    return HttpResponseRedirect(next)

                # 登录成功之后应该怎么返回页面
                return HttpResponseRedirect(reverse("index"))
            else:


                # 未查询到用户,还是保持原来的页面,  "login_form": login_form如果用户输入错误数据，则原封不动返回给用户
                return render(request, "login.html", {
                    "msg": "用户名或者密码错误",
                    "login_form": login_form,
                    "banners": banners,
                })

        else:
            # 如果用户名密码错误，则返回error给用户，是哪个字段没有填，会出红色框框
            return render(request, "login.html", {
                "login_form": login_form,
                "banners": banners,
            })






































