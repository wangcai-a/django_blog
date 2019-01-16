from django.urls import path
from . import views

app_name = 'comment'

# start with blog
urlpatterns = [
    path('', views.blog_comment, name='blog_comment')
]