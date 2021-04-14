# 提交表单在这里做
import re
from django import forms
from apps.operations.models import UserAsk


# 这个是用户提交用户咨询的
# 因为很多字段和model里一样，这里可以重载它
class AddAskForm(forms.ModelForm):
    # 手机号码一定要11位，这里要全覆盖掉在model的
    mobile = forms.CharField(max_length=11, min_length=11, required=True)

    # 要指明继承哪个model数据生成出来呢,那就用class Meta:
    class Meta:

        # 这个一一继承过来
        model = UserAsk

        # 指明要继承哪一个字段
        fields = ["name", "mobile", "course_name"]

    def clean_mobile(self):
        """
        验证手机号码是否合法

        """
        mobile = self.cleaned_data["mobile"]

        # 定义哪些电话是合格的
        regex_mobile = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(regex_mobile)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError("手机号码非法", code="mobile_invalid")





















