from django.db import models
from DjangoUeditor.models import UEditorField# 副文本


from apps.users.models import BaseModel
# models的作用就是表的定义,表结构的定义
# models就是设计字段的。这是授课机构的models


# 因为城市太多，如果以后想要添加就要改源代码，那就麻烦了，所以定义一个外键
# 这是外键,专门可以在后台可以添加我们的城市
class City(BaseModel):

    name = models.CharField(max_length=20, verbose_name=u"城市名")
    desc = models.CharField(max_length=200, verbose_name=u"描述")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

    # 这个str是添加数据的时候返回的一个主键，尽量存在
    def __str__(self):
        return self.name


# 授课机构
class CourseOrg(BaseModel):

    # 机构名称
    name = models.CharField(max_length=50, verbose_name=u"机构名称")

    # 描述
    # 课程详情就是一个副文本，这是引了第三方的插件DjangoUeditor,
    # 高度和宽度要设置好, 上传的图片放在imagePath="courses/ueditor/images/", 上传文件放在filePath="courses/ueditor/files"
    desc = UEditorField(verbose_name="描述", width=600, height=300, imagePath="courses/ueditor/images/",
                          filePath="courses/ueditor/files/", default="")

    # 机构标签
    tag = models.CharField(default="全国知名", max_length=10, verbose_name="机构标签")

    # 机构类别
    category = models.CharField(default="pxjg", verbose_name="机构类别", max_length=4, choices=(("pxjg", "培训机构"), ("gr", "个人"), ("gx", "高校")))

    # 点击数
    click_nums = models.IntegerField(default=0, verbose_name="点击数")

    # 收藏数
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")

    # 机构的图片
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"logo", max_length=100)

    # 机构地址
    address = models.CharField(max_length=150, verbose_name="机构地址")

    # 学习人数
    students = models.IntegerField(default=0, verbose_name=u"学习人数")

    # 课程数
    course_nums = models.IntegerField(default=0, verbose_name=u"课程数")

    # 所在城市
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="所在城市")

    # 是否金牌
    is_gold = models.BooleanField(default=False, verbose_name="是否金牌")

    # 是否认证
    is_auth = models.BooleanField(default=False, verbose_name="是否认证")

    # 去获取这个org的课程
    # 课程数
    def courses(self):

        # 这是第一种方法取外键，但有时候怕有些人会出现循环import错误，所以用第二种方法
        # 这句话不能写到全局，不然在courses全局调用了这个models,organizations双全局调用我们这个models，造成循环import,会出现错误
        # from apps.courses.models import Course
        #  # 查询下这个外键course_org
        # courses = Course.objects.filter(course_org=self)

        """
        这个是外键反取，course_set是怎么来呢，分两部分，
        1.course是Course方法的一个小写，也是调用这个Course方法
        2.那_set是怎么出现的呢，如果我们这个方法CourseOrg是Course的一个外键，那么就可以反向取，
        所以加起来就是course_set
        """
        courses = self.course_set.filter(is_classics=True)[:3]
        return courses

    # 得到全部的老师数量
    # 在course-detail.html中己经自己取全部的数量了
    # def teachers(self):
    #     """
    #     这个是外键反取，teacher_set是怎么来呢，分两部分，
    #     1.teacher是Teacher方法的一个小写，也是调用这个Teacher方法
    #     2.那_set是怎么出现的呢，如果我们这个方法CourseOrg是Course的一个外键，那么就可以反向取，
    #     所以加起来就是teacher_set
    #     """
    #     return self.teacher_set.all()


    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

    # 这个str是添加数据的时候返回的一个主键，尽量存在
    def __str__(self):
        return self.name


from apps.users.models import UserProfile
# 课程老师
class Teacher(BaseModel):
    # 定义一个外键，用户也能登录到我们的后台管理系统中，在courses/adminx下的NewCourseAdmin类的queryset方法己经定义了该返回的数据
    # 这个外键不再是ForeignKey，而是一个OneToOneField,一个teacher对应一个用户，是一对一的关系
    # 因为它己经有数据了， 可以指明为null=True
    user = models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="系统用户")

    # 所属机构
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构")

    # 教师名
    name = models.CharField(max_length=50, verbose_name=u"教师名")

    # 工作年限
    work_years = models.IntegerField(default=0, verbose_name="工作年限")

    # 就职公司
    work_company = models.CharField(max_length=50, verbose_name="就职公司")

    # 公司职位
    work_position = models.CharField(max_length=50, verbose_name="公司职位", null=True)

    # 教学特点
    points = models.CharField(max_length=50, verbose_name="教学特点")

    # 点击数量就是人气
    click_nums = models.IntegerField(default=0, verbose_name="点击数")

    # 收藏数
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")

    # 年龄
    age = models.IntegerField(default=18, verbose_name="年龄")

    # 头像
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100)

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    # 这个str是添加数据的时候返回的一个主键，尽量存在
    def __str__(self):
        return self.name

    # 添加一个能获取teacher的数量, 这是返回到org-detail-teacher中的课程数
    def course_nums(self):
        return self.course_set.all().count()



























