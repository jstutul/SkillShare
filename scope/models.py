from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
from django.urls import reverse

class ScopeManage(models.Model):
    SCOPE_TYPES = (
        ('Fellowship', 'Fellowship'),
        ('Internship', 'Internship'),
        ('Research Assistant', 'Research Assistant'),
        ('Teacher Assistant', 'Teacher Assistant'),
        ('Trainee', 'Trainee'),
    )

    user=models.ForeignKey(User, on_delete=models.CASCADE)
    scope_title=models.CharField(max_length=100, blank=False)
    category=models.CharField(choices=SCOPE_TYPES, max_length=30)
    post_date=models.DateTimeField(auto_now=True, auto_now_add=False)
    end_date=models.DateField(auto_now=False,auto_now_add=False)
    details = RichTextField()
    reactions = models.ManyToManyField(User, related_name="scope_like", blank=True)
    love = models.ManyToManyField(User, related_name="scope_love", blank=True)
    scope_viewer = models.ManyToManyField(User, blank=True, related_name="scope_viewer")
    scope_counter = models.IntegerField(default=0)
    cover_image=models.ImageField(upload_to="scope/", blank=False)
    url=models.URLField(blank=True)

    def __str__(self):
        return self.scope_title
    def total_reactions(self):
        return self.reactions.count()
    def total_love(self):
        return self.love.count()

    def get_absolute_url(self):
        return reverse("scopeview", kwargs={"category": self.category, "id": self.id})
    def get_absolute_url_manage(self):
        return reverse("managescope")

    def post_comment(self):
        post=ScopeComment.objects.filter(post=self).count()
        return post


class ScopeComment(models.Model):
    post = models.ForeignKey(ScopeManage,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reply = models.ForeignKey('ScopeComment',on_delete=models.CASCADE,null=True,related_name="replies")
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.scope_title,str(self.post.user))
