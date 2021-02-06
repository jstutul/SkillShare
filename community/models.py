from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80,blank=False)
    details = models.TextField(blank=False)
    post_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    def count_comment(self):
        c=BlogComment.objects.filter(post=self).count()
        return c
    def sub_count_comment(self):
        p=BlogComment.objects.filter(post=self)
        c=SubComment.objects.filter(post=self,comment=p).count()
        return c


class BlogComment(models.Model):
    post = models.ForeignKey(Blog,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    content = models.TextField(max_length=160)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)


class SubComment(models.Model):
    post = models.ForeignKey(Blog,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    comment =  models.ForeignKey(BlogComment,on_delete=models.CASCADE)
    content = models.TextField(max_length=160)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.content)
