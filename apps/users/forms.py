from django import forms
from captcha.fields import CaptchaField
import redis
from Mxonline.settings import REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile


# 个人中心修改手机号码的forms
class UpdateMobileForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=6, max_length=6)

    # clean_code是先于clean执行的
    # 这个函数名是forms提供的，能指明是哪一个字段出现了错误，只会认证我们的code
    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data


# 在views里ChangePwdView和这个form对应
# 这是要修改密码的一个form
class ChangePwdForm(forms.Form):
    # 自己要定义字段，因为UserProfile(AbstractUser)的字段是放在AbstractUser中的
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

    def clean(self):
        # 没有password1则为空字符
        # pwd1是新密码，pwd2是确认密码
        """
        cleaned_data的问题，改成用data.get()取值就好了，
        应该是因为前端传来的值都小于min_length，
        所以cleaned_data字典里没有值，然后取值取不到就报错
        """
        pwd1 = self.cleaned_data["password1"]
        pwd2 = self.cleaned_data["password2"]

        if pwd1 != pwd2:
            raise forms.ValidationError("密码不一致")
        # 如果改成功了那就返回一个
        return self.cleaned_data


# 个人中心修改用户信息, 定义好之后在views里面做功能
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        # 这是要修改的字段
        fields = ["nick_name", "gender", "birthday", "address"]


# 处理用户的上传头像问题
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]


# 注册的一个form,主要是返回图片验证码
class RegisterGetForm(forms.Form):
    captcha = CaptchaField()


# 第一：这个是注册的时候用来验证我们的手机验证码正不正确，第二点是密码
class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=6, max_length=6)
    password = forms.CharField(required=True)

    # 这是本来就有的一个函数，明确指明mobile已经注册
    def clean_mobile(self):
        mobile = self.data.get("mobile")
        # 验证手机号码是否已经注册
        users = UserProfile.objects.filter(mobile=mobile)
        if users:
            raise forms.ValidationError("该手机号已经注册")
        return mobile

    # clean_code是先于clean执行的
    # 这个函数名是forms提供的，能指明是哪一个字段出现了错误，只会认证我们的code
    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")

        return code


# 验证前端提交的数据表单
class LoginForm(forms.Form):
    # required = True代表着是否必填字段, min_length最小长度
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)


# 动态验证码的一个forms
class DynamicLoginForm(forms.Form):
    # 动态验证码的一个forms，必须要有几个字段，第一个是图片验证码，第二个是手机号码
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()


# login登录提交的一个forms
class DynamicLoginPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=6, max_length=6)

    # clean_code是先于clean执行的
    # 这个函数名是forms提供的，能指明是哪一个字段出现了错误，只会认证我们的code
    def clean_code(self):
        mobile = self.data.get("mobile")
        code = self.data.get("code")
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        redis_code = r.get(str(mobile))
        if code != redis_code:
            raise forms.ValidationError("验证码不正确")
        return self.cleaned_data


    # 做一些验证，验证是否有这个帐号和验证码的存在。要覆盖这个clean
    # def clean(self):
    #     mobile = self.cleaned_data["mobile"]
    #     code = self.cleaned_data["code"]
    #
    #     # 去redis里查询是否存在这个验证码
    #     r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
    #     redis_code = r.get(str(mobile))  # 获取手机和验证码
    #
    #     if code != redis_code:
    #         # 有问题就抛出异常
    #         raise forms.ValidationError("验证码不正确")
    #     # 没问题就
    #     return self.cleaned_data

















