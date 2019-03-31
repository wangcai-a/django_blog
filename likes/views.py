from django.shortcuts import render
from.models import LikeRecord, Likes, ContentType
from django.http import JsonResponse

# Create your views here.


def like_change(request):
    # 获取数据
    user = request.user

    # 判断用户是否登录
    if not user.is_authenticated:
        return errorResponse(400, "用户未登录,不能点赞")

    content_type = request.GET.get('content_type')
    object_id = request.GET.get('object_id')
    is_like = request.GET.get('is_like')
    content_type = ContentType.objects.get(model=content_type)

    # 处理数据
    if is_like == 'true':
        # 点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        if created:
            # 未点赞过,进行点赞
            like_count, created = Likes.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_num += 1
            like_count.save()
            return successRespoonse(like_count.like_num)
        else:
            # 已经点赞,不能重复点赞
            return errorResponse(402, '已经点赞过')
    else:
        # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有点赞过,取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            # 点赞数减1
            like_count, created = Likes.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_num -= 1
            like_count.save()
            return successRespoonse(like_count.like_num)
        else:
            # 没点赞过,不能取消
            return errorResponse(403, "没有点赞过,不能取消")


# 返回成功信息
def successRespoonse(like_num):
    data = {}
    data['status'] = "success"
    data['like_num'] = like_num
    return JsonResponse(data)


# 返回失败信息
def errorResponse(code, message):
    data = {}
    data['status'] = 'error'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

