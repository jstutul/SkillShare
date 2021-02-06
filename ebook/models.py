from django.contrib.auth.models import User
from django.db import models
from datetime import date,timedelta
BOOK_TYPE=(
        ('Free','Free'),
        ('Premium', 'Premium'),
    )
BOOK_Category =(
        ('Art & Music','Art & Music'),
        ('Biographies', 'Biographies'),
        ('Business','Business'),
        ('Comics','Comics'),
        ('Computer & Tech','Computer & Tech'),
        ('Cooking','Cooking'),
        ('Science & Technology','Science & Technology'),
        ('Entertainment','Entertainment'),
        ('Health & Fitness','Health & Fitness'),
        ('Hobbies & Craft','Hobbies & Craft'),
        ('Horror','Horror'),
        ('Kids','Kids'),
        ('Literature & Fiction','Literature & Fiction'),
        ('Medical','Medical'),
        ('Religion','Religion'),
        ('Romance','Romance'),
        ('Sci-Fi & Fantasy','Sci-Fi & Fantasy'),
        ('Science & Math','Science & Math'),
        ('Sports','Sports'),
        ('Travel','Travel'),
    )
# Create your models here.
class Ebook(models.Model):
    book_name = models.CharField(max_length=50, blank=False, null=False)
    book_author = models.CharField(max_length=30, blank=False, null=False)
    book_edition = models.PositiveIntegerField(default=1, blank=False)
    book_publish = models.DateField(auto_now=False, auto_now_add=False)
    category = models.CharField(choices=BOOK_Category, max_length=20, blank=False)
    book_type = models.CharField(choices=BOOK_TYPE, max_length=10, blank=False)
    cover_pic = models.ImageField(upload_to="ebook_cover/", blank=False)
    book = models.FileField(upload_to="ebooks/",blank=False)

    def __str__(self):
        return self.book_name
class Subscriber(models.Model):
    subscriber = models.ForeignKey(User,on_delete=models.CASCADE)
    until_date= models.DateField(blank=True,null=True)
    payment = models.FloatField(default=0)

    def __str__(self):
        return str(self.subscriber)
    def has_pad(self):
        current_date=date.today()
        if self.until_date > current_date:
            return True
