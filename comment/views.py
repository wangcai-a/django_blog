from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Blog
from .models import Comment
from .forms import CommentForm

# Create your views here.


def blog_comment(request, blog_pk):
    comment_blog = get_object_or_404(Blog, pk=blog_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)
            comment.blog = comment_blog

            # 保存评论数据
            comment.save()
            return redirect('/blog/%s' % blog_pk)
        else:
            # xx_set方法用来获取外键关联表的关联对象合集
            # blog.comment_set.all() 也等价于 Comment.objects.filter(blog=blog)
            comment_list = comment_blog.comment_set.all()
            context = {
                'blog': comment_blog,
                'form': form,
                'comment_list': comment_list,
            }
            return render(request, 'blog_detail.html', context=context)
    return redirect(comment_blog)
