# coding:utf-8
from django.http import Http404
from django.contrib.contenttypes.models import ContentType

from data.models import ReadDetail, ReadNum


# 阅读计数装饰器，需要指定模型类
def get_read_num(model_type):
    pass