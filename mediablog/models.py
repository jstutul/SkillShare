import tempfile

from django.contrib.auth.models import User
from django.contrib.sites import requests
from django.core import files
from django.db import models
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User

reaction_choices = (("like", "like"), ("heart", "heart"), ("sad", "sad"), ("haha", "haha"), ("angry", "angry"))


class Reaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(to="MediaBlog", on_delete=models.CASCADE)
    reaction_type = models.CharField(choices=reaction_choices, max_length=10)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return self.reaction_type
    # view_counter = models.ManyToManyField(to="view_count", related_name="viewcount",blank=True)

class MediaBlog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=80,blank=False)
    link = models.URLField(blank=False)
    media_description = RichTextField(null=True)
    thumbnail = models.ImageField(upload_to="mediablog/",blank=False)
    reactions = models.ManyToManyField(to=Reaction, related_name="reactions", blank=True)
    view_counter = models.ManyToManyField(User,blank=True,related_name="view_counter")
    counter=models.IntegerField(default=0)
    post_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    def count_view(self):
        return self.counter
    def total_reactions(self):
        return self.reactions.count()

    def like_count(self):
        return self.reactions.filter(reaction_type="like").count()

    def heart_count(self):
        return self.reactions.filter(reaction_type="heart").count()

    def angry_count(self):
        return self.reactions.filter(reaction_type="angry").count()

    def sad_count(self):
        return self.reactions.filter(reaction_type="sad").count()

    def haha_count(self):
        return self.reactions.filter(reaction_type="haha").count()
    def get_absolute_url(self):
        return reverse("mediadetails",kwargs={"id":self.id})

    def post_comment(self):
        post=Comment.objects.filter(post=self).count()
        return post

class Comment(models.Model):
    post = models.ForeignKey(MediaBlog,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reply = models.ForeignKey('Comment',on_delete=models.CASCADE,null=True,related_name="replies")
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.title,str(self.user.username))
