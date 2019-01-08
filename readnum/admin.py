from django.contrib import admin
from .models import ReadNum

# Register your models here.


@admin.register(ReadNum)
class ReadNum(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'read_num')
