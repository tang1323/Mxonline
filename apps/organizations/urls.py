from django.conf.urls import url
from apps.organizations.views import OrgView, AddAskView, OrgHomeView, OrgTeacherView, OrgCourseView, OrgDescView
from apps.organizations.views import TeacherListView, TeacherDetailView


# 授课机构下还有很多子url都放在这里，比如还有授课的详情页面等等，所以django用include机制做一个统一的处理
urlpatterns = [
    # 以$结束
    # 为了防止名字一样， 加上namespace="org"的作用是加上urls上的name="org_list"，所以就有org/list
    url(r'^list/$', OrgView.as_view(), name="list"),

    # 用户咨询, add_ask保持一致
    url(r'^add_ask/$', AddAskView.as_view(), name="add_ask"),


    # 在授课机构下，有很多org，所以要设计一个id，是动态的，例org/id
    # 如果我们用了这种org_id正则，那就会给view传一个参数
    # 授课机构下的一个课程机构的详情页面
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="home"),

    # 授课机构下的课程机构中的机构讲师,id也是动态的,用teacher做一个不同
    url(r'^(?P<org_id>\d+)/teacher/$', OrgTeacherView.as_view(), name="teacher"),

    # 授课机构下的课程机构中的机构课程
    url(r'^(?P<org_id>\d+)/course/$', OrgCourseView.as_view(), name="course"),

    # 机构介绍
    url(r'^(?P<org_id>\d+)/desc/$', OrgDescView.as_view(), name="desc"),


    # 这个是讲师列表页的url
    url(r'^teachers/$', TeacherListView.as_view(), name="teachers"),


    #
    # """
    # r'^/teachers/(?P<teacher_id>\d+)/$为什么把teacher_id放在后面，因为如果不这样放，
    # 会返回在前端不path会出现有/org/teachers，有/org/2/teachers，有/org/12/teachers
    # 所以这样放，那就只有/org/teachers，这样只有13个字符，选中状态就会跑到其他的模块下
    # 在base.html下94行和99行
    # 这里返回的path有好几种形式，有/org/teachers，有/org/2/teachers，有/org/12/teacher
    # """
    # 讲师详情页面
    url(r'^teachers/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name="teacher_detail"),
]




















