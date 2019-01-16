from django.shortcuts import redirect
from .models import Comment, ContentType
from django.http import Http404

# Create your views here.


def blog_comment(request):
    # 判断是否登录
    if not request.user.is_authenticated:
        return Http404
    text = request.POST['comment']
    # 判断是否提交空字符串
    if text.strip() == '':
        return Http404
    else:
        content_type = request.POST['content_type']
        object_id = request.POST['object_id']
        comment_user = request.user
    ct = ContentType.objects.get(model=content_type)
    comment_data = Comment(content_type=ct, object_id=object_id, text=text, comment_user=comment_user)
    comment_data.save()

    return redirect('blog:blog_detail', object_id)