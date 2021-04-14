
import xadmin

from apps.organizations.models import Teacher, CourseOrg, City
from apps.operations.models import Banner


# 全局的轮播图片
class BannerAdmin(object):
    # 在轮播图片的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["title", "image", "url", "index"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["title", "image", "url", "index"]

    # 过滤的字段, list_filter不要写错了
    list_filter = ["title", "image", "url", "index"]

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-mouse-pointer'


# adminx这里给后台生成一个表，一些超级用户可以管理这些表
# 可以不继承object
# 教师
class TeacherAdmin(object):
    # 在老师的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["org", "name", "work_years", "work_company"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["org", "name", "work_years", "work_company"]

    # 过滤的字段, list_filter不要写错了
    list_filter = ["org", "name", "work_years", "work_company"]

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-graduation-cap'


# 课程机构标签
class CourseOrgAdmin(object):
    # 在授课机构的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["name", "desc", "click_nums", "fav_nums"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["name", "desc", "click_nums", "fav_nums"]

    # 过滤的字段, list_filter不要写错了
    list_filter = ["name", "desc", "click_nums", "fav_nums"]

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-handshake-o'

    # 这个是要指明哪个字段要使用我们集成的一个副文本
    # desc表示副文本的字段
    # 前端记得加{% autoescape off %}{% endautoescape %}
    style_fields = {
        "desc": "ueditor",
    }


# 城市
class CityAdmin(object):
    # 在城市的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["id", "name", "desc"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["name", "desc"]

    # 过滤的字段, list_filter不要写错了
    list_filter = ["name", "desc", "add_time"]

    # 直接在列表页就可以修改名称之类的,工作大量修改就能减少点击时间
    list_editable = ["name", "desc"]

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-line-chart'


xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(City, CityAdmin)







