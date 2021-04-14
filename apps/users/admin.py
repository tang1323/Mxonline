from django.contrib import admin

# 这是一个创建用户的密码变成密文的一个管理器
from django.contrib.auth.admin import UserAdmin

from apps.users.models import UserProfile
# Register your models here.


class UserProfileAdmin(admin.ModelAdmin):
    pass


# 如果用了xadmin，注销掉也没有关系
# admin.site.register(UserProfile, UserAdmin)# 在后台管理生成一个表