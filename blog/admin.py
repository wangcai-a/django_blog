from django.contrib import admin
from .models import Blog, BlogType


# Register your models here.
@admin.register(BlogType)
class BlogType(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Blog)
class BlogArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "author", "is_deleted", "content", "created_time", "last_updated_time")
    ordering = ("id",)
