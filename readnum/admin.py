from django.contrib import admin
from .models import ReadNum

# Register your models here.


@admin.register(ReadNum)
class ReadNum(admin.ModelAdmin):
    list_display = ('id', 'read_num')
