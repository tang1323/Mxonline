from django.conf.urls import url


from apps.courses.views import CourseListView, CourseDetailView, CourseLessonView, CourseCommentsView
from apps.courses.views import VideoView

# 课程下还有很多子url都放在这里，比如还有授课的详情页面等等，所以django用include机制做一个统一的处理
urlpatterns = [
    # 以$结束
    # 为了防止名字一样， 加上namespace="course"的作用是加上urls上的name="course_list"，所以就有org/list
    # 首先要进入课程的列表页
    url(r'^list/$', CourseListView.as_view(), name="list"),

    # 在课程公开课下，有很多course，所以要设计一个id，是动态的，例course/id
    # 如果我们用了这种course_id正则，那就会给view传一个参数
    # 公开课下的一个课程公开的详情页面
    url(r'^(?P<course_id>\d+)/$', CourseDetailView.as_view(), name="detail"),

    # 课程的章节信息url
    url(r'^(?P<course_id>\d+)/lesson/$', CourseLessonView.as_view(), name="lesson"),

    # 课程评论
    url(r'^(?P<course_id>\d+)/comments/$', CourseCommentsView.as_view(), name="comments"),

    #
    url(r'^(?P<course_id>\d+)/video/(?P<video_id>\d+)$', VideoView.as_view(), name="video"),

]




















