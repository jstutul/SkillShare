from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render,redirect
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode

from accounts.models import contactUs
from mediablog.models import *
from events.models import *
from scope.models import  *
from ebook.models import  *
from journal.models import *
import datetime
from django.core.mail import send_mail, EmailMessage


def HomeView(request):
    medias = MediaBlog.objects.all().order_by('-id')[:2]
    popular = MediaBlog.objects.all().order_by('-id')[2:5]
    events = EventManager.objects.all().order_by('-id').filter(end_date__gte=datetime.date.today())[:2]
    popular_pop = EventManager.objects.all().order_by('-id').filter(end_date__gte=datetime.date.today())[2:5]
    scope = ScopeManage.objects.all().order_by('-id')[:2]
    popular_scope = ScopeManage.objects.all().order_by('-id')[2:5]
    ebooks =Ebook.objects.all().order_by('-id')[:4]
    jourl = Journal.objects.all().order_by('-id')[:4]
    context = {
        'medias':medias,
        'popular':popular,
        'events': events,
        'popular_event':popular_pop,
        'scope':scope,
        'popular_scope':popular_scope,
        'ebooks':ebooks,
        'journal':jourl,
    }
    return render(request,'index.html',context)

def contactview(request):
    if request.method=="POST":
        fullname_ =request.POST.get("fullname")
        email_ =request.POST.get("email")
        phone_=request.POST.get("phone")
        company_=request.POST.get("company")
        message_=request.POST.get("message")
        contactUs(
            fullname=fullname_,email=email_,phone=phone_,company=company_,message=message_
        ).save()
        subject = 'Contact Us'
        message = render_to_string('extra/contact.html', {
            'user': fullname_,
        })
        to_email = email_
        email = EmailMessage(
            subject, message, to=[to_email]
        )
        email.send()
        email = EmailMessage(
            subject, message_, to=[settings.EMAIL_HOST_USER,]
        )
        email.send()
        messages.info(request,"Your message is send successfully.Be patient for admin reply")
        return render(request,'extra/06_contact-us.html',{'message':messages})
    else:
        return render(request,'extra/06_contact-us.html')
def aboutview(request):
    return render(request,'extra/aboutus.html')
