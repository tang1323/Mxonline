
import xadmin

from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag, BannerCourse
from xadmin.layout import Fieldset, Main, Side, Row     # 页面布局修改的


# 改下左上角的标题和页脚
class GlobalSettings(object):
    site_title = "幕课后台管理系统"
    site_footer = "幕课在线网"
    # 把一些models合起来，量大可以设置
    # menu_style = "accordion"


# 这是开启主题皮肤功能
class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True


# 多张表一次性编辑，这是课程的章节
class LessonInline(object):
    # 这里model指向models里的Lesson类
    model = Lesson
    # 这个是设置成一个标题的形式，更加简洁，但是跟课程里面的资源有bug。所以一般注释掉
    # style = "tab"
    extra = 0
    # 隐藏时间
    exclude = ["add_time"]


# 课程的资源，在models里一定要跟Course有外键依赖才能写进来
class CourseResourceInline(object):
    # 这里model指向models里的CourseResource类
    model = CourseResource
    style = "tab"
    extra = 1
    # 隐藏时间
    exclude = ["add_time"]


# 写同一个管理器管理同一个管理器会报错的，所以我们再生成一个Course,只是我们都指向了一张表
# 这个是在courses/models的BannerCourse类
# 轮播课程
class BannerCourseAdmin(object):
    # 通过这个类做不同的管理
    # 在课程的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["name", "desc", "detail", "degree", "learn_times", "students"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["name", "desc", "detail", "degree", "students"]

    # 过滤的字段, list_filter不要写错了,双下划就代表着把这个teacher的name进行一个过滤，这是一个外键过滤
    list_filter = ["name", "teacher__name", "desc", "detail", "degree", "learn_times", "students"]

    # 直接在列表页就可以修改名称之类的,工作大量修改就能减少点击时间
    list_editable = ["degree", "desc"]
    # 这是从NewCourseAdmin拿过来的，可以一样，也可以不一样

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-braille'

    # 同一张表不同数据，那我们就做一个过滤
    # 自己定义要返回哪些一数据回来
    def queryset(self):
        # queryset()这个默认返回所有的数据
        qs = super().queryset()
        # 做一个过滤，必须是is_banner=True的才行，就是认为是轮播课程为True
        qs = qs.filter(is_banner=True)
        return qs


# admin这里给后台生成注册一个表，一些超级用户可以管理这些表
# 可以不继承object
class CourseAdmin(object):
    # 在课程的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["name", "desc", "detail", "degree", "learn_times", "students"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["name", "desc", "detail", "degree", "students"]

    # 过滤的字段, list_filter不要写错了,双下划就代表着把这个teacher的name进行一个过滤，这是一个外键过滤
    list_filter = ["name", "teacher__name", "desc", "detail", "degree", "learn_times", "students"]

    # 直接在列表页就可以修改名称之类的,工作大量修改就能减少点击时间
    list_editable = ["degree", "desc"]


# 这个是xadmin的导入导出功能
from import_export import resources


# 课程
class MyResource(resources.ModelResource):
    class Meta:
        # 导入导出具体的字段是在Course下的字段，在models下有个Course类，是要导入导出这些字段
        model = Course
        # fields = ('name', 'description',)
        # exclude = ()


# 课程信息
# 这个是给xadmin的课程信息的编辑页面进行一个优化
class NewCourseAdmin(object):

    # 这是导入导出功能的配置
    import_export_args = {'import_resource_class': MyResource, 'export_resource_class': MyResource}

    # 在课程的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["name", "desc", "detail", "degree", "learn_times", "students", 'show_image', 'go_to', ]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["name", "desc", "detail", "degree", "students"]

    # 过滤的字段, list_filter不要写错了,双下划就代表着把这个teacher的name进行一个过滤，这是一个外键过滤
    list_filter = ["name", "teacher__name", "desc", "detail", "degree", "learn_times", "students"]

    # 直接在列表页就可以修改名称之类的,工作大量修改就能减少点击时间
    list_editable = ["degree", "desc"]

    # 在后台只能为可读状态的字段
    readonly_fields = ["click_nums", "fav_nums", "students", "add_time"]

    # 这个是在新增的时候是看不到的一个字段，有默认值就能写在这，这个字段和可读的字段不能重复
    # Fieldset也不能和这个发生冲突，只能有一个存在，所以这个先注释掉
    # exclude = ["click_nums", "fav_nums", "students"]

    # 这个是排序
    ordering = ["-click_nums"]

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-leanpub'

    # 在models里必须是有外键的存在的， 它外键指向Course,这样就能在CourseAdmin配置，这样就能在多张表上一次性编辑
    # 在这个页面有个LessonInline类，条件如上才能写到这，用inlines字段表示
    inlines = [LessonInline, CourseResourceInline]

    # 这个是要指明哪个字段要使用我们集成的一个副文本
    # detail表示副文本的字段
    # 前端记得加{% autoescape off %}{% endautoescape %}
    style_fields = {
        "detail": "ueditor",
    }



    # 自己定义要返回哪些一数据回来
    def queryset(self):
        # queryset()这个默认返回所有的数据
        qs = super().queryset()

        # 获取当前的用户，如果是超级用户，那就返回所有的数据
        # 如果是其他用户，比如teacher，那就返回它属于它自己的数据
        # 这句话判断是否是超级用户，如果是，那就返回所有的数据, 如果不是，那就返回teacher的数据
        # 但是在teacher要有一个外键，一个用户对就一个teacher
        if not self.request.user.is_superuser:
            # user可以反向取红色的那个teacher，因为是一对一的关系
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs

    # 改造页面布局的方法
    def get_form_layout(self):
        # 加上这个是编辑页面才执行我们以下的逻辑，点击增加课程是没有这个修改之后的页面的
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset("讲师信息",
                             "teacher", 'course_org',
                             css_class='unsort no_title'
                             ),
                    Fieldset("基本信息",
                             "name", 'desc',
                             # 这个是放在一行的几个字段
                             Row('learn_times', 'degree'),
                             Row('category', 'tag'),
                             'youneed_know', 'teacher_tell', 'detail'
                             )

                ),
                # Side的意思是显示在右边的内容
                Side(
                    Fieldset("访问信息",
                             'fav_nums', 'click_nums', 'students', 'add_time'
                             ),
                ),
                Side(
                    Fieldset("选择信息",
                             'is_banner', 'is_classics'
                            ),
                )
            )
        return super(NewCourseAdmin, self).get_form_layout()


# 课程章节
class LessonAdmin(object):
    # 在课程的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["course", "name", "add_time"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["course", "name"]

    # 过滤的字段, list_filter不要写错了,为什么加下划，加了之后可以对课程名称可以有个过滤
    list_filter = ["course__name", "name", "add_time"]

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-folder-open'


# 视频
class VideoAdmin(object):
    # 在视频的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["lesson", "name", "add_time"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["lesson", "name"]

    # 过滤的字段, list_filter不要写错了
    list_filter = ["lesson", "name", "add_time"]

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-video-camera'


# 课程资源
class CourseResourceAdmin(object):
    # 在课程资源的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["course", "name", "file", "add_time"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["course", "name", "file"]

    # 过滤的字段, list_filter不要写错了
    list_filter = ["course", "name", "file", "add_time"]

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-paper-plane'


# 课程标签
class CourseTagAdmin(object):
    # 在课程标签的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["course", "tag", "add_time"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["course", "tag"]

    # 过滤的字段, list_filter不要写错了
    list_filter = ["course", "tag", "add_time"]

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-magic'


# xadmin.site.register(Course, CourseAdmin)

# 上面的CourseAdmin修改布局成了NewCourseAdmin， 只能要一个
# 这是修改xadmin布局的一个NewCourseAdmin课程信息
xadmin.site.register(Course, NewCourseAdmin)

# 这是一个管理器管理不同的两个管理器的一个注册, 这两个是我们配置的xadmin，要注意
xadmin.site.register(BannerCourse, BannerCourseAdmin)

xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseTag, CourseTagAdmin)

# 把左上角的标题和页脚注册进来
xadmin.site.register(xadmin.views.CommAdminView, GlobalSettings)

# 注册全局主题皮肤
xadmin.site.register(xadmin.views.BaseAdminView, BaseSettings)
















