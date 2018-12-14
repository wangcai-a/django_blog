from django.shortcuts import render, get_object_or_404
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
import markdown

# Create your views here.
from django.http import HttpResponse, Http404
from .models import Blog, BlogType


def blog_list(request):
    context = {}
    context['blogs'] = Blog.objects.filter(is_deleted=False)
    context['blogs_count'] = Blog.objects.filter(is_deleted=False).count()
    context['blog_types'] = BlogType.objects.all()
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

    context = {
        'blog': article,
        'blog_toc': md.toc,
        'blog_types': BlogType.objects.all()
    }
    return render(request, 'blog_detail.html', context)


def blog_with_type(request, blog_type_id):
    context = {}
    blog_type = get_object_or_404(BlogType, id=blog_type_id)
    context['blogs'] = Blog.objects.filter(blog_type=blog_type)
    context['blog_type'] = blog_type
    context['blog_types'] = BlogType.objects.all()
    return render(request ,'blog_with_type.html', context)