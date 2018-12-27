from django.urls import path, re_path
from . import views

app_name = 'comment'

# start with blog
urlpatterns = [
    re_path('^blog/(?P<blog_pk>[0-9]+)/$', views.blog_comment, name='blog_comment')
]