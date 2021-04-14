

from django.db import models


from django.db import models
from datetime import datetime
from apps.users.models import BaseModel
from apps.organizations.models import Teacher
from apps.organizations.models import CourseOrg

from DjangoUeditor.models import UEditorField# 副文本


# models的作用就是表的定义,表结构的定义
# 1.设计表结构有几个重要的点
"""
实体1<关系>实体2
课程(Course) --一对多-- 章节(Lesson) --一对多-- 视频(video)   课程资源(CourseResource)


"""
# 2.实体的具体字段

# 3.每个字段的类型，是否必填


# 课程
class Course(BaseModel):
    # 这是个外键，指向的是我们的Teacher，  是一个课程讲师,跟在organizations的models是链接在一起的，是一个关系
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师")

    # 这里隔了一个外键，是相对比较麻烦的了所以加一个外键直接指向我们的CourseOrg,为了查询方便
    # 在这里直接加一个外键直接指向我们的CourseOrg
    course_org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="课程机构", null=True, blank=True)

    # 定义课程信息
    name = models.CharField(verbose_name="课程名", max_length=50)

    # 课程描述
    desc = models.CharField(verbose_name="课程描述", max_length=300)

    # 课程时长，尽量设置小的单位，比如分钟和秒
    learn_times = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")

    # 课程难度
    degree = models.CharField(verbose_name="难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)

    # 学习人数
    students = models.IntegerField(default=0, verbose_name="学习人数")

    # 收藏人数
    fav_nums = models.IntegerField(default=0, verbose_name="收藏人数")

    # 点击数
    click_nums = models.IntegerField(default=0, verbose_name="点击数")

    # 课程公告
    notice = models.CharField(verbose_name="课程公告", max_length=300, default="")

    # 课程类别
    category = models.CharField(default=u"后端开发", max_length=20, verbose_name="课程类别")

    # 课程标签
    tag = models.CharField(default="", verbose_name="课程标签", max_length=10)

    # 课程须知
    youneed_know = models.CharField(default="", max_length=300, verbose_name="课程须知")

    # 老师告诉你
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="老师告诉你")

    # 怎么显示是经典课程呢
    is_classics = models.BooleanField(default=False, verbose_name="是否经典")

    # 课程详情就是一个副文本，这是引了第三方的插件DjangoUeditor,
    # 高度和宽度要设置好, 上传的图片放在imagePath="courses/ueditor/images/", 上传文件放在filePath="courses/ueditor/files"
    detail = UEditorField(verbose_name="课程详情", width=600, height=300, imagePath="courses/ueditor/images/", filePath="courses/ueditor/files/", default="")

    # 这个是广告（轮播图片）的课程还是网站的课程
    is_banner = models.BooleanField(default=False, verbose_name="是否广告位")

    # 课程图片
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", max_length=100)

    class Meta:
        verbose_name = "课程信息"
        verbose_name = verbose_name

    # 这个str是添加数据的时候返回的一个主键，尽量存在
    def __str__(self):
        return self.name

    # 如果要新增一个字段，要加一个models，那要更新数据库，那就要很麻烦
    # 如果删除一个章节还要减一，那就要改的地方很多
    # 这里就是动态的来统计一下，定义一个函数
    def lesson_nums(self):
        # 对章节做一个统计
        return self.lesson_set.all().count()

    # 这个是要在xadmin显示的时候要显示出图片来，就是要把一个路径自己拼接成一个html
    # show_image要配置到当前adminx下
    def show_image(self):
        from django.utils.safestring import mark_safe
        # self.image.url, 就是这个类下的image
        return mark_safe("<img src='{}'>".format(self.image.url))
    # 这是定义一个显示的名称
    show_image.short_description = "图片"

    # 点击这个课程图片，他能跳转到当前的课程的页面
    def go_to(self):
        from django.utils.safestring import mark_safe
        # self.image.url, 就是这个类下的image
        return mark_safe("<a href='/course/{}'>跳转</a>".format(self.id))
    # 这是定义一个显示的名称
    go_to.short_description = "跳转"


# 这是同一张表的不同数据使用不同的管理器进行管理
# 说白了就是两个管理器集中在一起管理
# 因为是管理轮播图片的课程，所以要继承Course
class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name = verbose_name

        # 加上这个migrate就不会再生成一张表,我们只是想对多个管理器进行一个管理而已
        proxy = True


# 课程标签
class CourseTag(BaseModel):
    # 现在来定义一些外键, 用ForeignKey,是一些实体... on_delete表示对应的外键数据被删除后，当前的数据应该怎么办
    # 外键课程
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")

    # 课程标签
    tag = models.CharField(max_length=100, verbose_name="标签")

    class Meta:
        verbose_name = "课程标签"
        verbose_name = verbose_name

    # 这个str是添加数据的时候返回的一个主键，尽量存在, 是不能为null
    def __str__(self):
        return self.tag


# 章节
class Lesson(BaseModel):

    # 现在来定义一些外键, 用ForeignKey,是一些实体... on_delete表示对应的外键数据被删除后，当前的数据应该怎么办
    # 外键课程
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")# on_delete=models.SER_NULL, null=True, blank=True也行

    name = models.CharField(max_length=100, verbose_name=u"章节名")

    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")

    class Meta:
        verbose_name = "课程章节"
        verbose_name = verbose_name

    # 这个str是添加数据的时候返回的一个主键，尽量存在
    def __str__(self):
        return self.name


# 视频
class Video(BaseModel):
    # Video和Lesson是外键关系的

    # 章节
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.CASCADE)

    # 视频名
    name = models.CharField(max_length=100, verbose_name=u"视频名")

    # 学习时长
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长(分钟数)")

    # 视频网址
    url = models.CharField(max_length=1000, verbose_name=u"访问地址")

    class Meta:
        verbose_name = "视频"
        verbose_name = verbose_name

    # 这个str是添加数据的时候返回的一个主键，尽量存在
    def __str__(self):
        return self.name


# 课程资源
class CourseResource(BaseModel):

    # 外键课程
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")

    # 名称
    name = models.CharField(max_length=100, verbose_name=u"名称")

    # 上传文件
    file = models.FileField(upload_to="course/resourse/%Y/%m", verbose_name="下载地址", max_length=200)

    class Meta:
        verbose_name = "课程资源"
        verbose_name = verbose_name

    # 这个str是添加数据的时候返回的一个主键，尽量存在
    def __str__(self):
        return self.name





















