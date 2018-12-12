from django.templatetags.static import static
from django.urls import reverse

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': static,
        'url': reverse,
    })
    return env

# 修改setting.py文件 'BACKEND': 'django.template.backends.jinjia2.jinja2'
# 并在OPTIONS中添加 'environment': 'Django_blog.jinja2.environment', 即可切换为jinja模板