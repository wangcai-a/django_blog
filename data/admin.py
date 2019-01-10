from django.contrib import admin
from .models import ReadDetail, ReadNum

# Register your models here.


@admin.register(ReadNum)
class ReadNum(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'read_num')


@admin.register(ReadDetail)
class BlogType(admin.ModelAdmin):
    list_display = ('id', 'requested_at', 'ip_address', 'user')