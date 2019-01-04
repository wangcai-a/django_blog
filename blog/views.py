from django.shortcuts import render, get_object_or_404
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
import markdown
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from comment.forms import CommentForm

# Create your views here.
from django.http import HttpResponse, Http404
from .models import Blog, BlogType


def blog_list(request):
    context = {}
    blogs = Blog.objects.filter(is_deleted=False)

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
    context['paginator'] = paginator
    context['blogs'] = contacts
    context['blogs_count'] = Blog.objects.filter(is_deleted=False).count()
    context['blog_types'] = BlogType.objects.all()
    context['now_page'] = int(page)
    return render(request ,'blog_list.html', context)


def blog_detail(request, blog_id):
    md = markdown.Markdown(extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                     TocExtension(slugify=slugify)
                                        ])
    article = get_object_or_404(Blog, pk=blog_id)

    article.content = md.convert(article.content)

    # 打开增加一个阅读数
    article.read_num += 1
    article.save()

    # 获取这篇文字的评论
    form = CommentForm()
    comment_list = article.comment_set.all()

    context = {
        'blog': article,
        'blog_toc': md.toc,
        'blog_types': BlogType.objects.all(),
        'blog_comments': comment_list,
        'form': form
    }
    response = render(request, 'blog_detail.html', context)
    response.set_cookie('blog_%s_read' % blog_id, 'true', max_age=300)
    return response


def blog_with_type(request, blog_type_id):
    context = {}
    blog_type = get_object_or_404(BlogType, id=blog_type_id)
    blogs = Blog.objects.filter(blog_type=blog_type)
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
    context['paginator'] = paginator
    context['blogs'] = contacts
    context['blogs_count'] = Blog.objects.filter(blog_type=blog_type).count()
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    context['now_page'] = int(page)
    return render(request, 'blog_with_type.html', context)