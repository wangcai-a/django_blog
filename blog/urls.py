from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('<int:article_id>', views.article_detail, name='article_detail'),
    path('', views.article_list, name='article_list')
]