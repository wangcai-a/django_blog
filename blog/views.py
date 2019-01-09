from django.shortcuts import render, get_object_or_404
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
import markdown
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from comment.forms import CommentForm
from django.db.models import Q
from django.db.models.fields import exceptions

# Create your views here.
from django.http import HttpResponse, Http404
from .models import Blog, BlogType
from readnum.models import ContentType, ReadNum


def blog_list(request):
    blogs = Blog.objects.filter(is_deleted=False)
    context = get_list_detail(request, blogs)
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

    ct = ContentType.objects.get_for_model(Blog)
    try:
        re = ReadNum.objects.get(content_type=ct, object_id=blog_id)
        # 通过cookies判断是否增加阅读数
        if not request.COOKIES.get('blog_%s_read' % blog_id):
            re.read_num += 1
    except exceptions.ObjectDoesNotExist:
        re = ReadNum(content_type=ct, object_id=blog_id, read_num=1)
    re.save()

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
    # 设置cookies,过期时间设为300秒
    response.set_cookie('blog_%s_read' % blog_id, 'true', max_age=300)
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
        'now_page': int(page)
    }
    return context
