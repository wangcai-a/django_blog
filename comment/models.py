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
    comment_user = models.ForeignKey(User, related_name="comments",on_delete=models.DO_NOTHING)

    root_id = models.IntegerField(default=0)
    parent = models.ForeignKey('self', null=True, on_delete=models.DO_NOTHING)
    reply_to = models.ForeignKey(User, null=True, related_name='replies', on_delete=models.DO_NOTHING)    # 回复的评论或者账号名称

    def __str__(self):
        return self.text[:20]