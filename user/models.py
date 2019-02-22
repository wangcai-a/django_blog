from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


# 继承自带的用户模型
class User(AbstractUser):
    nickname = models.CharField(max_length=10, blank=True)

    class Meta(AbstractUser.Meta):
        pass


# 用户验证
class User_ex(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    vaild_code = models.IntegerField(max_length=24)
    vaild_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % (self.valid_code)