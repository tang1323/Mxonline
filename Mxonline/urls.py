"""Mxonline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.views.generic import RedirectView   # 可视化的包
import xadmin
# from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt    # 去除csrf_token的验证

from django.views.static import serve   # 静态文件的处理方法(图片也行)

from apps.users.views import LoginView, LogoutView, SendSmsView, DynamicLoginView, RegisterView

from Mxonline.settings import MEDIA_ROOT

# 这个是首页的view
from apps.operations.views import IndexView

urlpatterns = [


    # url模式相对来说更加强大，因为支持正则表达式
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    # 可视化路由
    # url('echart/', include('smart_chart.echart.urls')),
    # url('', RedirectView.as_view(url='echart/index/')),  # 首页,可自定义路由

    path('', IndexView.as_view(), name="index"),
    path('login/', LoginView.as_view(), name="login"),  # 登录接口
    path('register/', RegisterView.as_view(), name="register"),     # 这是register注册的页面配置
    path('d_login/', DynamicLoginView.as_view(), name="d_login"),   # 动态登录
    path('logout/', LogoutView.as_view(), name="logout"),   # 退出接口
    url(r'^captcha/', include('captcha.urls')),     # 图像验证码

    # csrf_exempt去除csrf_token的验证, 一般我们不会去掉这个验证，有时候前后端分离才会去掉
    url(r'^send_sms/', csrf_exempt(SendSmsView.as_view()), name="send_sms"),    # 验证码的url,send_sms要跟login.js里面的url必须一致

    # 配置上传文件和访问的url，图片的设置,, document_root就是文件的根路径
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    # 404页面
    # url(r'^static/(?P<path>.*)$', serve, {"document_root": STATIC_ROOT}),

    # 机构相关页面的配置
    # 只要是以org开头的所有子路径都放在operations.urls文件中
    # 为了防止名字一样， 加上namespace="org"的作用是加上urls上的name="org_list"，所以就有org/list
    url(r'^org/', include(('apps.organizations.urls', "organizations"), namespace="org")),

    # 课程相关url
    # courses要跟apps文件下的courses文件名保持一致
    url(r'^course/', include(('apps.courses.urls', "courses"), namespace="course")),

    # 用户相关操作
    url(r'^op/', include(('apps.operations.urls', "operations"), namespace="op")),


    # 用户个人中心
    url(r'^users/', include(('apps.users.urls', "users"), namespace="users")),

    # 配置副文本的相关url
    url(r'^ueditor/', include('DjangoUeditor.urls')),
]

# 现在登录要提交数据那有两个方式，强烈建议使用CBV
# 1.CBV(class base view)    2.FBV(function base view)


# 编写一个view的几个步骤
"""
1. view代码
2. 配置url
3. 修改html页面中相关的地址
"""















