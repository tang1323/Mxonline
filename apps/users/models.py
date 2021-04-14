from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

# models的作用就是表的定义,表结构的定义
# 有一些数据库没有用户的字段，比如：昵称之类，现在继承这个类AbstractUser，就可以往里加一些字段


GENDER_CHOICES = (
    ("male", "男"),
    ("female", "女")
)


# 添加课程的时间,因为要多次调用，所以单独放在这
class BaseModel(models.Model):
    # 添加课程的时间,因为要多次调用，所以单独放在这
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    # 为 什么要class Meta，因为BaseModels继承了models.Model，会生成一个表，如果设置一下abstract = True，那就不会生成表
    class Meta:
        abstract = True


# 这个原本在数据库有个叫auth_user,现在是重新定义一个自己的user
# 函数名自己定义，但一般叫UserProfile，但一定要继承AbstractUser这个对象
class UserProfile(AbstractUser):
    # 昵称字段， 一开始是没有昵称的，所以default可以为空，两个都可以
    # nick_name = models.CharField(max_length=50, verbose_name="昵称", null=True, blank=True)
    nick_name = models.CharField(max_length=50, verbose_name="昵称", default="")

    # 生日
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)

    # 性别
    gender = models.CharField(verbose_name="性别", choices=GENDER_CHOICES, max_length=6)

    # 地址
    address = models.CharField(max_length=100, verbose_name="地址", default="")

    # 手机号码,unique=True一个手机号码只能注册一次,这里先把它取消掉
    mobile = models.CharField(max_length=11, verbose_name="手机号码")

    # 头像, 这个是用户放的头像upload_to="head_image/%Y/%m"，是放在media里。。。刚创建的默认头像default="default.jpg"，
    image = models.ImageField(verbose_name="用户头像", upload_to="head_image/%Y/%m", default="default.jpg")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    # 这是未读的消息的数量
    def unread_nums(self):
        # 外键反向取, usermessage_set就是这个函数UserMessage
        # 在UserMessage定义了是否己读的字段has_read
        return self.usermessage_set.filter(has_read=False).count()

    # 得到这些字段后的描述是什么，怎么处理
    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            # 如果继承了AbstractUser，那就必须填这个username
            return self.username


        


















