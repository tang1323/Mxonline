"""
Django settings for Mxonline project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '##&c-ge#vjs*)j*o9&ntt+9e#23u2yt0x57a6in43eprow4*j-'

# SECURITY WARNING: don't run with debug turned on in production!

# 这个是在开必过程中才能设置为True,上线部署后就要设置为False
# 因为在开发的时候有错误它能抛出错误栈出来
DEBUG = True

# '*'为全部网址
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # 美化后台ui
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.courses.apps.CoursesConfig',  # 课程模块的配置
    'apps.users.apps.UsersConfig',  # 用户模块的配置
    'apps.organizations.apps.OrganizationsConfig',  # 机构相关模块的配置
    'apps.operations.apps.OperationsConfig',    # 用户操作模块的配置
    'xadmin.apps.XAdminConfig',     # 配置xadmin
    'crispy_forms',     # 配置xadmin

    'captcha',  # 图片验证码的加入
    'pure_pagination',  # 课程分页功能
    'DjangoUeditor',    # 副文本的配置
    'import_export',    # xadmin的导入和导出

    # 数据可视化
    # 'smart_chart.echart',





]

AUTHENTICATION_BACKENDS = [
    "apps.users.views.CustomAuth"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 加入smart_chart.echart要注释掉这个
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Mxonline.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # 全局配置在html中
                'django.template.context_processors.media',

                # 这是全局未读消息,写在users/views,类似上面的media
                'apps.users.views.message_nums'

            ],
        },
    },
]

WSGI_APPLICATION = 'Mxonline.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        # mysql的配置,使用mysql
        'ENGINE': 'django.db.backends.mysql',

        # 这是我们在mysql数据库建的一个数据库名称
        'NAME': "mxonline",
        # 连接的用户名和密码
        "USER": "tangming",
        "PASSWORD": "130796",
        "HOST": "127.0.0.1"

    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# AUTH_USER_MODEL = "apps.users.models.UserProfile"# 用下面的写法，因为INSTALLED_APPS里己经写了
# 在uesr下中的models.py里定义了一个类UserProfile，是自己定义给数据的用户字段，在这里要配置
# 原本在makemigrations后在数据库有个表叫auth_user表，现在我们觉得不好用，重新自己定义一个
# 所以这里需要重新配置一下
AUTH_USER_MODEL = "users.UserProfile"



# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

# 这是后台管理显示英文的
# LANGUAGE_CODE = 'en-us'

# 这是后台管理显示中文的
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True
# 此处必须为False
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/


# STATIC_ROOT和STATICFILES_DIRS只能同时出现一个
# 一般我们是打开STATICFILES_DIRS，在部署的时候STATIC_ROOT才有用
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    # os.path.join(BASE_DIR, 'apps/message_form/static'),
]

# STATIC_ROOT和STATICFILES_DIRS只能同时出现一个
# 这个变量一定要注释掉，在部署的时候才有用,才能打开
# STATIC_ROOT = os.path.join(BASE_DIR, "static")


# 云片网相关设置
yp_apikey = "3b4b90283fa8e7caae18876077f7b08b"


#redis相关配置
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379

#1.如果重启django 变量不存在
#2.随着验证码越来越多，内存占用越来越大，验证码过期
#3. redis k-v, 设计一个过期时间，过期就删除掉



# 图片的设置
MEDIA_URL = "/media/"
# 指明上传的文件放在哪一个目录之下
MEDIA_ROOT = os.path.join(BASE_DIR, "media")




# 课程分页功能的配置
# PAGE_RANGE_DISPLAYED是指能看到有几页
# MARGIN_PAGES_DISPLAYED当页数过多时，能看到几个前后页数
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 5,
    'MARGIN_PAGES_DISPLAYED': 2,

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}















