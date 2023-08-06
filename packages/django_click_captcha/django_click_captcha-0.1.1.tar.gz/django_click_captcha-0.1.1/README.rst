点击倒字验证码
==========================

简介
--------

点击倒字验证码，仿照知乎验证码效果实现， 用户通过点击验证码上面的倒着的汉字， 从而通过验证码验证。

环境条件
------------

* Python>=3.4
* Django>=1.9


安装
----------

Using pip::

    $ pip install django_click_captcha

or from source code::

    $ pip install -e git+https://github.com/malongge/click_captcha.git#egg=click_captcha

将 click_captcha 加到 INSTALL_APPS 列表当中

使用方法
--------

配置:

CLICK_CAPTCHA_WIDGET_TEMPLATE: 验证码模板代码， 默认为 `click_captcha/captcha.html`

CLICK_CAPTCHA_TIMEOUT: 验证码过期时间， 默认为 60 秒

CACHE_BACKEND: 验证码缓存服务， 默认为数据库: `django.core.cache.backends.db.DatabaseCache`

因此如果使用默认的缓存服务，需要执行下面的命令 `python manage.py createcachetable` 创建缓存表


urls.py 添加获得验证码的地址::

    from django.conf.urls import url

    from click_captcha import views

    urlpatterns = [
        url(r'click_captcha/(?P<uuid>\w+)/$', views.CaptchaView.as_view(), name='click_captcha'),
    ]

加载样式标签::

    { % load click_captcha_tags % }
    ...
    { % include_click_captcha_css  False % }
    ...
    { % include_click_captcha_js False % }


如果希望用安装包自带的 bootstrap 和 jquery 去掉 False 参数

添加 form 表单， 比如 admin 登录配置::

    from django.contrib.admin.forms import (
    AdminAuthenticationForm as _AdminAuthenticationForm
    )
    from django.forms import ValidationError

    from click_captcha.fields import CaptchaField


    class AuthenticationForm(_AdminAuthenticationForm):
        field_order = ['captcha', 'username', 'password']

        captcha = CaptchaField()

        def _clean_fields(self):
            for name, field in self.fields.items():
                value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))
                try:
                    value = field.clean(value)
                    self.cleaned_data[name] = value
                    if hasattr(self, 'clean_%s' % name):
                        value = getattr(self, 'clean_%s' % name)()
                        self.cleaned_data[name] = value
                except ValidationError as e:
                    self.add_error(name, e)
                    return

这里 _clean_fields 是想先进行验证码校验， 如果验证码校验不成功就不进行用户和密码的验证码了

新建个 sites.py, 替换原来的 login form::

    from django.contrib.admin.sites import AdminSite as _AdminSite

    from apps.authentication.forms import AuthenticationForm
    from apps.authentication.models import User

    class MyAdminSite(_AdminSite):
        login_form = AuthenticationForm
        login_template = 'click_captcha/login.html'


    admin_site = MyAdminSite(name='myadmin')
    admin_site.register(User)

在 login.html 中加上验证码 form 字段::

    { % load click_captcha_tags %}

    { % block extrastyle %}
        { % include_click_captcha_css  False %}
    { % endblock %}

    ... ...
    { # form 表单下插入 #}
       <div class="{ % if form.captcha.errors %} error{ % endif %}">
            {{ form.captcha }}
       </div>
    ... ...
    { % block extrajs %}
      { % include_click_captcha_js False %}
    { % endblock %}

效果图
------

.. image:: https://malongge.github.io/assets/django/captcha-django.gif
    :target: https://malongge.github.io/2017/08/04/django-zhihu-captcha-4-read.html


备注信息
---------

该项目不支持 python 2 版本， django 版本必需高于 django 1.9

该项目有一系列文章的介绍其是如何开发的过程， 可以参考文章来定制自己的验证码

`博客地址 <https://malongge.github.io/blog/>`_

