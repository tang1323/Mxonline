from django.conf.urls import url

from apps.operations.views import AddFavView, CommentView

# 用户操作下还有很多子url都放在这里，比如还有授课的详情页面等等，所以django用include机制做一个统一的处理
urlpatterns = [
    # 以$结束
    # 为了防止名字一样， 加上namespace="org"的作用是加上urls上的name="org_list"，所以就有org/list
    # 用户收藏操作

    # 前端的页面也要做一个url配置，这个是是org_base中的ajax
    url(r'^fav/$', AddFavView.as_view(), name="fav"),

    # 评论提交
    url(r'^comment/$', CommentView.as_view(), name="comment"),
]




















