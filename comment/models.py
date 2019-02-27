from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from user.models import User

# Create your models here.


class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    comment_user = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    root_id = models.IntegerField(default=0)
    parent_id = models.IntegerField(default=0)
    reply_name = models.CharField(max_length=50, blank=True)    # 回复的评论或者账号名称

    def __str__(self):
        return self.text[:20]