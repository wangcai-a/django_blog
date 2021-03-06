from django.urls import path
from . import views

app_name = 'blog'

# start with blog
urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:id>', views.blog_detail, name='blog_detail'),
    path('type/<int:blog_type_id>', views.blog_with_type, name='blog_with_type'),
    path('search/', views.blog_search, name='blog_search')
]