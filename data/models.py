from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from user.models import User

# Create your models here.


class ReadNum(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    read_num = models.IntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')


class ReadDetail(models.Model):
    # content_type关联字段
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    content_object = GenericForeignKey('content_type', 'object_id')
    object_id = models.PositiveIntegerField()
    # 普通字段
    requested_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(blank=True, max_length=15)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)