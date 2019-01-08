from django.db import models
from user.models import User
from mdeditor.fields import MDTextField
from readnum.models import ContentType, ReadNum

# Create your models here.


# 博文类型
class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return "%s" % self.type_name


# 博文模型
class Blog(models.Model):
    title = models.CharField(max_length=30)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = MDTextField()
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(Blog)
            re = ReadNum.objects.filter(content_type=ct, object_id=self.pk)
            return re[0].read_num
        except:
            return 0

    def __str__(self):
        return "%s" % self.title

    class Meta():
        ordering = ['-created_time']