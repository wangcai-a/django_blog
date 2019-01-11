# coding:utf-8
from django.http import Http404
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions

from data.models import ReadDetail, ReadNum


# 阅读计数装饰器，需要指定模型类
def get_read_num(model_type):
    def __get_read_num(func):
        def wapper(request, id):
            try:
                obj = model_type.objects.get(id=id)
            except exceptions.ObjectDoesNotExist:
                raise Http404

            # 获取模型名称作为cookies键名
            model_name = str(model_type).split("'")[1].split(".")[-1]
            cookie_name = "%s_%s_read" % (model_name, id)

            # 判断是否需要增加一条记录
            if not request.COOKIES.get(cookie_name):
                # 添加明细记录
                read_detail = ReadDetail(content_object=obj)
                read_detail.ip_address = request.META.get("HTTP_X_FORWARDED_FOR", request.META.get("REMOTE_ADDR", None))
                if request.user.is_authenticated:
                    read_detail.user = request.user
                else:
                    read_detail.user = None
                read_detail.save()

                # 总记录加1
                ct = ContentType.objects.get_for_model(obj)
                read_num = ReadNum.objects.filter(content_type=ct, object_id=obj.id)

                if read_num.count() > 0:
                    readnum = read_num[0]
                else:
                    readnum = ReadNum(content_type=ct, object_id=obj.id)
                readnum.read_num += 1
                readnum.save()

            # 执行原来的方法
            response = func(request, id)

            # 添加cookies,300秒过期,300秒内只计算一个阅读量
            response.set_cookie(cookie_name, 'True',max_age=300)
            return response
        return wapper
    return __get_read_num