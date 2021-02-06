from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from ckeditor.fields import RichTextField
JOURNAL_TYPE=(
        ('Data mining','Data mining'),
        ('Science', 'Science'),
        ('Technology', 'Technology'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
        ('Machine Learning', 'Machine Learning'),
    )
DOCUMENT_TYPE=(
        ('Pdf','Pdf'),
        ('Doc', 'Doc'),
    )
J_TYPE=(
        ('Free','Free'),
        ('Paid', 'Paid'),
    )
rating_choices = (("1", 1), ("2", 2), ("3", 3), ("4", 4), ("5", 5))

class RatedJournal(models.Model):
    user_r = models.ForeignKey(User, on_delete=models.CASCADE)
    journal_r = models.ForeignKey(to="Journal", on_delete=models.CASCADE)
    ratting_r = models.IntegerField(validators=[MaxValueValidator(5),MinValueValidator(1)],default=1)

    class Meta:
        unique_together = ("user_r", "journal_r")
        index_together=(("user_r", "journal_r"))

    def __str__(self):
        return str(self.ratting_r)
    def total_rating(self):
        return sum(self.ratting_r)
class Journal(models.Model):
    post_by=models.ForeignKey(User,on_delete=models.CASCADE)
    journal_title=models.CharField(max_length=60,blank=False)
    journal_details=RichTextField(default="enter something for details")
    jornal_author=models.CharField(max_length=30,blank=False)
    publication_year=models.DateField(auto_now_add=False)
    journal_category=models.CharField(choices=JOURNAL_TYPE,max_length=40)
    document_type=models.CharField(choices=DOCUMENT_TYPE,max_length=10)
    jornal_cover=models.ImageField(upload_to="journal/",blank=False)
    journal_type=models.CharField(choices=J_TYPE,max_length=10)
    price=models.PositiveIntegerField(default=0.0,blank=True)
    post_date=models.DateTimeField(auto_now_add=True)
    journal_view=models.ManyToManyField(User,related_name="journal_view",blank=True)
    journal_file=models.FileField(upload_to="journal_file/",blank=False)
    download_count = models.IntegerField(blank=True, default=0)
    access = models.ManyToManyField(User, related_name="journal_access", blank=True)



    def __str__(self):
        return self.journal_title
    def total_acces(self):
        return int(self.access.count())
    def no_of_rating(self):
        ratings=RatedJournal.objects.filter(journal_r=self)
        return len(ratings)

    def avg_ratings(self):
        sum=0
        a = []
        ratings=RatedJournal.objects.filter(journal_r=self)
        for r in ratings:
            a.append(str(r))
        for i in a:
            sum+=int(i)
        print(sum)
        if len(ratings)>0:
            return sum/len(ratings)
        else:
            return 0
    def get_absolute_url(self):
        return reverse("journaldetails", args=[self.journal_title, self.id])
class JournalOrder(models.Model):
    journal=models.ForeignKey(Journal,max_length=100,null=True,blank=True,on_delete=False)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.journal.journal_title
class JournalPayment(models.Model):
    jouenal_owner=models.ForeignKey(User,on_delete=models.Case)
    income=models.FloatField(default=0.0)

    def __str__(self):
        return str(self.jouenal_owner)
class RequestWithdraw(models.Model):
    request_user=models.ForeignKey(User,on_delete=models.CASCADE)
    paypal = models.EmailField(max_length=20,blank=False,null=True)
    payment = models.FloatField(default=0)

    def __str__(self):
        return str(self.request_user)
class JournalComment(models.Model):
    post = models.ForeignKey(Journal,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reply = models.ForeignKey('JournalComment',on_delete=models.CASCADE,null=True,related_name="replies")
    content = models.TextField(max_length=160)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.post.journal_title,str(self.post.post_by))
