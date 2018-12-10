from django.urls import path
from . import views

app_name = 'blog'

# start with blog
urlpatterns = [
    path('<int:blog_id>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_type_id>', views.blog_with_type, name='blog_with_type'),
]