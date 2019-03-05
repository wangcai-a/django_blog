from django.shortcuts import render, get_object_or_404
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
import markdown
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.
from .models import Blog, BlogType
from data.models import ContentType
from comment.models import Comment
from comment.forms import CommentForm

from data.decorator import get_read_num


def blog_list(request):
    blogs = Blog.objects.filter(is_deleted=False)
    context = get_list_detail(request, blogs)
    return render(request, 'blog_list.html', context)


@get_read_num(Blog)
def blog_detail(request, id):
    md = markdown.Markdown(extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                     TocExtension(slugify=slugify)
                                        ])
    article = get_object_or_404(Blog, pk=id)

    article.content = md.convert(article.content)

    # 获取这篇文字的评论
    ct = ContentType.objects.get_for_model(Blog)
    comment_list = Comment.objects.filter(content_type=ct, object_id=id, root=None)
    form_data = {
        'content_type': ct.model,
        'object_id':  id,
        'reply_comment_id': 0,
    }
    comment_form = CommentForm(initial=form_data)

    context = {
        'blog': article,
        'blog_toc': md.toc,
        'blog_types': BlogType.objects.all(),
        'blog_comments': comment_list.all(),
        'comment_form': comment_form,
    }
    response = render(request, 'blog_detail.html', context)
    return response


def blog_with_type(request, blog_type_id):
    blog_type = get_object_or_404(BlogType, id=blog_type_id)
    blogs = Blog.objects.filter(blog_type=blog_type)
    context = get_list_detail(request, blogs)
    return render(request, 'blog_with_type.html', context)


def blog_search(request):
    q = request.GET.get('q')
    if not q:
        err_msg = '请输入关键词'
        return render(request, 'blog_list.html', {'err_msg': err_msg})
    blogs = Blog.objects.filter(Q(title__icontains=q) | Q(content__icontains=q))
    context = get_list_detail(request, blogs)
    return render(request, 'blog_list.html', context=context)


def get_list_detail(request, blogs):
    paginator = Paginator(blogs, 10)
    page = request.GET.get('page')
    if page is None:
        page = 1
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    context = {
        'paginator': paginator,
        'blogs': contacts,
        'blogs_count': Blog.objects.filter(is_deleted=False).count(),
        'blog_types': BlogType.objects.all(),
        'now_page': int(page),
    }
    return context
