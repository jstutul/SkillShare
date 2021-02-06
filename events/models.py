from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
from django.urls import reverse


class EventManager(models.Model):
    EVENT_TYPES = (
        ('Local', 'Local'),
        ('International', 'International'),
        ('Others', 'Others'),
    )
    event_title = models.CharField(max_length=50,null=False)
    event_organizar=models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(choices=EVENT_TYPES,max_length=15)
    description=RichTextField(blank=False)
    interested =models.ManyToManyField(User, related_name='interested',blank=True)
    start_date =models.DateField(auto_now=False)
    end_date =models.DateField(auto_now=False)
    start_time =models.TimeField(auto_now=False)
    end_time =models.TimeField(auto_now=False)
    seat_limit =models.PositiveIntegerField(default=0)
    entry_fee =models.PositiveIntegerField(default=0)
    location =models.CharField(max_length=50)
    post_on=models.DateTimeField(auto_now_add=True)
    registration_link=models.URLField(blank=False)
    event_view = models.ManyToManyField(User, blank=True, related_name="event_view")
    view_count = models.IntegerField(default=0)
    banner =models.ImageField(upload_to='Event/',blank=False)

    def __str__(self):
        return self.event_title

    def total_interested(self):
        return self.interested.count()

    def get_absolute_url(self):
        return reverse("eventdetails", kwargs={"category":self.category,"id": self.id})

class EventComment(models.Model):
    post = models.ForeignKey(EventManager,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reply = models.ForeignKey('EventComment',on_delete=models.CASCADE,null=True,related_name="replies")
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.event_title,str(self.post.event_organizar))
