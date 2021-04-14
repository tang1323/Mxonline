from django.conf.urls import url
# 这个可以代替我们在views的功能, 这是django自带的
from django.views.generic import TemplateView
# 这个是登录才能有访问的装饰器
from django.contrib.auth.decorators import login_required


from apps.users.views import UserInfoView, UploadImageView, ChangePwdView, ChangeMobileView
from apps.users.views import MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

# 课程下还有很多子url都放在这里，比如还有授课的详情页面等等，所以django用include机制做一个统一的处理
urlpatterns = [
    # 以$结束
    # 为了防止名字一样， 加上namespace="users"的作用是加上urls上的name="users_info"，所以就有users/info
    # 首先是用户的信息
    url(r'^info/$', UserInfoView.as_view(), name="info"),

    # 解决头像的上传
    url(r'^image/upload/$', UploadImageView.as_view(), name="image"),

    # 在个人中心里修改用户密码的一个子url
    url(r'^update/pwd/$', ChangePwdView.as_view(), name="update_pwd"),

    # 在个人中心修改手机号码
    url(r'^update/mobile/$', ChangeMobileView.as_view(), name="update_mobile"),

    # 个人资料我的课程
    # url(r'^mycourse/$', MyCourseView.as_view(), name="mycourse"),


    # 个人资料我的课程, 这个是更加高级的用法,用Django本身自带的TemplateView做
    # # 选中的状态定义{"current_page":"mycourse"}
    # login_required()没登录是访问不了我的课程的,
    # login_url="/login/"在没有登录的情况下,你想访问我的课程,它会把你跳到指定的页面

    url(r'^mycourse/$', login_required(TemplateView.as_view(template_name="usercenter-mycourse.html"), login_url="/login/"), {"current_page": "mycourse"}, name="mycourse"),

    # 个人中心下的我的收藏下的课程机构
    url(r'^myfavorg/$', MyFavOrgView.as_view(), name="myfavorg"),

    # 个人中心下的我的收藏下的授课教师
    url(r'^myfav_teacher/$', MyFavTeacherView.as_view(), name="myfav_teacher"),

    # 个人中心下的我的收藏下的公开课程
    url(r'^myfav_course/$', MyFavCourseView.as_view(), name="myfav_course"),

    # 个人中心下的我的消息
    url(r'^messages/$', MyMessageView.as_view(), name="messages"),

]




















