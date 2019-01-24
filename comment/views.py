from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment, ContentType
from .forms import CommentForm

# Create your views here.


def blog_comment(request):

    comment_form = CommentForm(request.POST, user=request.user)
    if comment_form.is_valid():
        # 检测通过,保存数据
        comment_user = request.user
        content_type = comment_form.cleaned_data['content_type']
        text = comment_form.cleaned_data['comment']
        object_id = comment_form.cleaned_data['object_id']
        ct = ContentType.objects.get(model=content_type)
        comment_data = Comment(content_type=ct, object_id=object_id, text=text, comment_user=comment_user)
        comment_data.save()
        data = {
            'status': 'success',
            'username': comment_data.comment_user.username,
            'comment_time': comment_data.created_time.strftime('%Y-%m-%d %H:%M:%S'),
            'comment': comment_data.text,
        }
    else:
        data = {
            'status': 'error',
            'message': list(comment_form.errors.values())[0][0]
        }
    return JsonResponse(data)