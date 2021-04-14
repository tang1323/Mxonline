# 提交表单在这里做
import re
from django import forms
from apps.operations.models import UserFavorite, CourseComments


# 这个是用户收藏和取消收藏的相关操作
# 因为很多字段和model里一样，这里可以重载它
class UserFavForm(forms.ModelForm):

    # 要指明继承哪个model数据生成出来呢,那就用class Meta:
    class Meta:

        # 这个一一继承过来
        model = UserFavorite

        # 指明要继承哪一个字段
        fields = ["fav_id", "fav_type"]


# 用户在章节里面的评论
class CommentsForm(forms.ModelForm):

    # 要指明继承哪个model数据生成出来呢,那就用class Meta:
    class Meta:
        # 这个一一继承过来
        model = CourseComments

        # 指明要继承哪一个字段, course注意是一个外键
        fields = ["course", "comments"]


















