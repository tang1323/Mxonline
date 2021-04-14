from django.db import models

from django.contrib.auth import get_user_model# 调用这个就知道在是否用户有登录了，在seetings有配置，
UserProfile = get_user_model()

from apps.courses.models import Course
from apps.users.models import BaseModel
# Create your models here.
# 用户的一些操作,models的作用就是表的定义,表结构的定义


# 全局的轮播图
class Banner(BaseModel):
    # 轮播的名称
    title = models.CharField(max_length=100, verbose_name="标题")

    # 轮播的图片
    image = models.ImageField(upload_to="banner/%Y/%m", max_length=200, verbose_name="轮播图片")

    # 这个轮播图的一个url是一个跳转，也可以跳到授课机构的url
    url = models.URLField(max_length=200, verbose_name="访问地址")

    # 轮播图也是有顺序的，哪个是第一个，第二个
    index = models.IntegerField(default=0, verbose_name="顺序")
    class Meta:
        verbose_name = "轮播图片"
        verbose_name_plural = verbose_name

    # 这个str是添加数据的时候返回的一个主键，尽量存在
    def __str__(self):
        return self.title


# 记录用户提交的咨询
class UserAsk(BaseModel):
    name = models.CharField(max_length=20, verbose_name="姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    course_name = models.CharField(max_length=50, verbose_name=u"课程名", null=True)

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    # 这个str是添加数据的时候返回的一个主键，尽量存在
    def __str__(self):
        return "{name}_{course}({mobile})".format(name=self.name, course=self.course_name, mobile=self.mobile)


# 课程相关的评论
class CourseComments(BaseModel):

    # 定义我们的外键，必须有这个登录才能评论， 用户
    # 是外键就要设计一个on_delete,不然会出错
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")

    # 这个也是我们的外键,课程
    # 是外键就要设计一个on_delete,不然会出错
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")

    # 评论内容，能评论200个字符
    comments = models.CharField(max_length=200, verbose_name="评论内容")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    # 这个str是添加数据的时候返回的一个主键，尽量存在
    def __str__(self):
        return self.comments


# 用户收藏夹
class UserFavorite(BaseModel):

    # 定义我们的外键，必须有这个登录才能收藏， 用户
    # 是外键就要设计一个on_delete,不然会出错
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")

    # 课程,为了防止网站体量越大，就用fav_id来指定
    fav_id = models.IntegerField(verbose_name="数据id")

    # 收藏类型
    fav_type = models.IntegerField(choices=((1, "课程"), (2, "课程机构"), (3, "讲师")), default=1, verbose_name=u"收藏类型")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    # 这个str是添加数据的时候返回的一个主键，尽量存在
    def __str__(self):
        return "{user}_{id}".format(user=self.user.username, id=self.fav_id)


# 用户的消息
class UserMessage(BaseModel):
    # 定义我们的外键，必须有这个登录才能看到消息， 用户
    # 是外键就要设计一个on_delete,不然会出错
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")

    message = models.CharField(max_length=200, verbose_name="消息内容")

    # 如果有消息发来，那就有一个铃铛，如果点开了，那么消息就为0了, default=False就是还没有读的消息
    has_read = models.BooleanField(default=False, verbose_name=u"是否己读")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    # 这个str是添加数据的时候返回的一个主键，尽量存在
    def __str__(self):
        return self.message


# 用户和课程之间的关系, 一个课程可以被多个用户学习，就是多对多的关系
# 先定义一对多的关系
class UserCourse(BaseModel):
    # 定义我们的外键，必须有这个登录才能看到自己的课程， 用户
    # 是外键就要设计一个on_delete,不然会出错
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")

    # 这个也是我们的外键,课程
    # 是外键就要设计一个on_delete,不然会出错
    course = models.ForeignKey(Course, on_delete=models.CASCADE,  verbose_name="课程")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course.name

















