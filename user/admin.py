from django.contrib import admin
from .models import User


# Register your models here.
@admin.register(User)
class BlogArticleAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "date_joined")
    ordering = ("id",)
