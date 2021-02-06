import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from ebook.models import *
# Create your views here.
def EHome(request):
    return render(request,'ebook/Ehome.html')

def CategoryView(request,cat):

    books=[]
    is_book=False
    is_book_more=False
    b=Ebook.objects.all().filter(category=cat).order_by('-id')
    if len(b) > 6:
        is_book=True
        for i in b[:6]:
            books.append(i)
    elif len(b)==0:
        pass
    else:
        is_book=True
        for i in b[:len(b)]:
            books.append(i)


    next_book=[]
    bk=Ebook.objects.all().filter(category=cat).order_by('-id')
    if len(bk) > 6:
        is_book_more=True
        for i in bk[7: len(bk)]:
            next_book.append(i)


    context={
        'books':books,
        'category':cat,
        'next_book':next_book,
        'is_books':is_book,
        'is_book_more':is_book_more,
    }
    return render(request, 'ebook/viewcategory.html', context)


@login_required(login_url='login')
def Readbook(request,book_name):
    book = Ebook.objects.get(book_name=book_name)
    print(book.book)
    context = {
        'book': book,
    }
    if book.book_type=="Free":
        return render(request,'ebook/readbook.html',context)
    elif book.book_type=="Premium":
        if request.user.is_superuser:
            return render(request, 'ebook/readbook.html', context)
        else:
            if Subscriber.objects.filter(subscriber=request.user).exists():
                user=Subscriber.objects.get(subscriber=request.user)
                if user.has_pad() == True:
                    return render(request, 'ebook/readbook.html', context)

                else:
                    messages.info(request, "Your Subscription is out of date .Please subscribe new package to read premium books")
                    return render(request, 'ebook/subscription.html')
            else:
                return render(request,'ebook/subscription.html')

def Subscription(request):
    return render(request,'ebook/subscription.html')
def Checkout(request,pack):
    print(pack)
    package =""
    price =0.0
    if pack=="1M":
        package= "30  Days"
        price = price+ 20.0

    elif pack=="3M":
        package= "3 Month"
        price = price + 50.0

    elif pack=="12M":
        package= "1 Year"
        price = price + 100.0
    user=request.user
    context ={
        'pack':package,
        'price':price,
        'username':user,
    }


    return render(request,'ebook/checkout.html',context)

def SubscriptionCompleted(request):
    body = json.loads(request.body)
    user=(body['subscription_user'])
    pack =(body['packname'])
    current_date =date.today()
    subs=''
    price=0
    if pack == "30  Days":
        days = timedelta(days=30)
        subs = current_date + days
        price = 20
    elif pack == "3 Month":
        days = timedelta(days=90)
        subs = current_date + days
        price = 50
    elif pack == "1 Year":
        days = timedelta(days=366)
        subs = current_date + days
        price = 100
    try:
        if Subscriber.objects.filter(subscriber=get_object_or_404(User,username=user)).exists():
            user=Subscriber.objects.get(subscriber=get_object_or_404(User,username=user))
            print(current_date, user.until_date)
            if user.until_date < current_date:
                user.until_date = subs
                user.payment += price
                user.save()
                print("done")
        else:
            new=Subscriber.objects.create(
                subscriber=get_object_or_404(User,username=user),
                until_date=subs,
                payment=price

            )
            new.save()


    except:
        pass
    return JsonResponse('Sunscription completed',safe=False)
