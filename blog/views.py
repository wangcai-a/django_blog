from django.shortcuts import render, get_object_or_404, render_to_response

# Create your views here.
from django.http import HttpResponse, Http404
from .models import Blog


def article_detail(request, article_id):
    article = get_object_or_404(Blog, pk=article_id)
    context = {
        'article_obj': article
    }
    return render(request, 'article_detail.html', context)


def article_list(request):
    articles = Blog.objects.filter(is_deleted=False)
    context = {
        'articles': articles
    }
    return render_to_response('article_list.html', context)