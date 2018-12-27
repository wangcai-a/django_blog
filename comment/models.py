from django.db import models

# Create your models here.


class Comment(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)

    blog = models.ForeignKey('blog.Blog', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.text[:20]