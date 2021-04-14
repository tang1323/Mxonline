import xadmin

from apps.operations.models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse


# 用户咨询
class UserAskAdmin(object):
    # 在记录用户提交的咨询的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["name", "mobile", "course_name", "add_time"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["name", "mobile", "course_name", "add_time"]

    # 过滤的字段, list_filter不要写错了
    list_filter = ["name", "mobile", "course_name", "add_time"]

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-envelope'


# 用户课程
class UserCourseAdmin(object):
    # 在用户和课程之间的关系的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["user", "course", "add_time"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["user", "course"]

    # 过滤的字段, list_filter不要写错了
    list_filter = ["user", "course", "add_time"]

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-tasks'

    # 这是一个保存过程的一个拦截
    # 用户学习课程的记录做一个保存， 在这个类没有继承什么，那到底哪些方法可以重载呢
    # 凡是在xadmin中有@filter_hook都可以重载
    def save_models(self):
        # 当我们新一个记录的时候，它会生一个记录
        obj = self.new_obj
        # 我们新增一个数据的id是为None的，如果是编辑的页面是为1的
        # 所以新增一个数据课程人数才加1，如果是修改编辑的我们就认为你没有增加
        if not obj.id:
            # 对象没有id的时候，先保存下对象
            obj.save()
            # 然后再找到当前的obj的对象course
            course = obj.course
            course.students += 1
            course.save()
        # 在这后面也可以加一些message，可以向用户发送消息"欢迎学习该课程"


# 用户消息
class UserMessageAdmin(object):
    # 在用户和课程之间的关系的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["user", "message", "has_read", "add_time"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["user", "message", "has_read"]

    # 过滤的字段, list_filter不要写错了
    list_filter = ["user", "message", "has_read", "add_time"]

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-comments'


# 课程评论
class CourseCommentsAdmin(object):
    # 在课程相关的评论的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["user", "course", "comments", "add_time"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["user", "course", "comments"]

    # 过滤的字段, list_filter不要写错了
    list_filter = ["user", "course", "comments", "add_time"]

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-meh-o'


# 用户收藏
class UserFavoriteAdmin(object):
    # 在用户收藏夹的列表页要显示哪一些字段, 要跟定义的字段对应起来, list_display不要写错了
    list_display = ["user", "fav_id", "fav_type", "add_time"]

    # 要在后台搜索哪一些字段,desc字段是描述的意思，search_fields不要写错了
    search_fields = ["user", "fav_id", "fav_type"]

    # 过滤的字段, list_filter不要写错了
    list_filter = ["user", "fav_id", "fav_type", "add_time"]

    # 这个是对后台管理的图标设置
    # 百度，这个图标库叫awesome font，现在是放在xadmin/static/vendor/font-awesome下的两个css和js
    model_icon = 'fa fa-gavel'


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)




















