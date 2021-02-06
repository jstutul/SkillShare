import json
import os
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.db.models import Q, F
from django.http import JsonResponse, HttpResponse
from urllib.parse import quote_plus
from django.shortcuts import render,redirect,get_object_or_404,Http404
from django.template.loader import render_to_string
from django.http import FileResponse
from journal.models import Journal,JournalOrder,RatedJournal,JournalComment,JournalPayment,RequestWithdraw
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from journal.forms import *
def JournalHome(request):
    journals = Journal.objects.all().order_by('-id')
    trends = Journal.objects.all().order_by('-download_count')
    print(trends)
    query = request.GET.get('q')
    if query:
        journals = journals.filter(
            Q(journal_title__icontains=query) |
            Q(journal_category__icontains=query) |
            Q(post_by__username__icontains=query)
        ).distinct()
    paginator = Paginator(journals, 6)
    page = request.GET.get('page')
    journals = paginator.get_page(page)

    context ={
        'journals': journals,
        'trends': trends[:10],
    }
    return render(request,'journal/journalhome.html',context)
def JournalDetails(request,title,id):
    if request.user.is_authenticated:
        journal = get_object_or_404(Journal,id=id)
        share_string=quote_plus(journal.journal_details)
        if journal.journal_view.filter(id=request.user.id).exists():
            pass
        else:
            journal.journal_view.add(request.user)
        popular_journal = Journal.objects.all().order_by('-journal_view').order_by('download_count')

        my_rating = RatedJournal.objects.filter(journal_r=journal.id,user_r=request.user)

        ratting=0
        for r in my_rating:
            if r.user_r == request.user:
                ratting = r.ratting_r
            else:
                ratting = 0
        is_access=False
        if journal.access.filter(id=request.user.id).exists():
            is_access=True
        comments = JournalComment.objects.filter(post=journal, reply=None).order_by('-id')
        if request.method=="POST":
            comment_form =CommentForm(request.POST or None)
            if comment_form.is_valid():
                content = comment_form.cleaned_data.get('content')
                reply_id = request.POST.get('comment_id')
                comment_qs = None
                if reply_id:
                    comment_qs = JournalComment.objects.get(id=reply_id)
                comment = JournalComment.objects.create(post=journal,user=request.user,content=content,reply=comment_qs)
                comment.save()
                # return redirect(event.get_absolute_url())
        else:
            comment_form = CommentForm()
        context={
            'journal':journal,
            'is_access':is_access,
            'ratting':ratting,
            'comments': comments,
            'comment_form': comment_form,
            'popular_journal':popular_journal[:7],
            'share_string':share_string,
        }
        if request.is_ajax():
            html = render_to_string('journal/journal_comment_section.html',context,request=request)
            return JsonResponse({'form':html})
        return render(request,'journal/journaldetails.html',context)
    else:
        return redirect('login')

def Download(request):
    Journal.objects.filter(id=request.POST.get('journal_id')).update(download_count=F('download_count')+1)
    journal = get_object_or_404(Journal, id=request.POST.get('journal_id'))
    absolute_file_path = journal.journal_file.path
    file_name, file_extension = os.path.splitext(journal.journal_file.name)
    response = FileResponse(open(absolute_file_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename= "{}"'.format(f"{file_name.split('/')[-1]}{file_extension}")
    journal.save()
    context = {
        'journal': journal,
    }
    if request.is_ajax():
        html = render_to_string('journal/journal_download.html', context, request=request)
        return JsonResponse({'form': html})
def Checkout(request,id):
    journal=Journal.objects.get(id=id)
    context ={
        'journal':journal,
    }
    return render(request,'journal/checkout.html',context)
def paymentComplated(request):
    body=json.loads(request.body)
    print('BODY',body)
    journal_new = Journal.objects.get(id=body['journalId'])
    if journal_new.access.filter(id=request.user.id).exists():
        pass
    else:
        journal_new.access.add(request.user)
    value=journal_new.price
    JournalOrder.objects.create(
        journal=journal_new,
    )
    try:
        if JournalPayment.objects.filter(jouenal_owner=journal_new.post_by).exists():
            print("ki")
            JournalPayment.objects.filter(jouenal_owner=journal_new.post_by).update(income=F('income') + value)
            print("hoyse")
        else:
            print("yeah")
            new_payment=JournalPayment.objects.create(
                jouenal_owner=get_object_or_404(User,username=journal_new.post_by),income=value
            )
            new_payment.save()
            print("baby")
    except:
        pass
    # return JsonResponse('payment completed',safe=False)
    return redirect('Mainhome')
def download_journal(request, journal_id):
    try:
        file = Journal.objects.get(id=journal_id)
    except Journal.DoesNotExist:
        return HttpResponse("file not found")
    absolute_file_path = file.journal_file.path
    file_name, file_extension = os.path.splitext(file.journal_file.name)
    response = FileResponse(open(absolute_file_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename= "{}"'.format(f"{file_name.split('/')[-1]}{file_extension}")
    file.download_count = F('download_count') + 1
    file.save()
    return response
def Rated(request):
    journal=get_object_or_404(Journal,id=request.POST['journal_id'])
    rating=request.POST['ratings']
    if journal.rated_by.filter(id=request.user.id).exists():
        print("yes")
    else:
        journal.rated_by.add(request.user)
        journal.user_rating=rating

    return redirect(journal.get_absolute_url())

def AddRatting(request):
    journal_id=request.POST['jour']
    j=Journal.objects.get(id=journal_id)
    try:
       if RatedJournal.objects.filter(journal_r=j,user_r=request.user).exists():
           rate = RatedJournal.objects.get(journal_r=j, user_r=request.user)
           rate.ratting_r = request.POST['rat']
           rate.save()
       else:
            RatedJournal.objects.create(
                journal_r=j,
                user_r=request.user,
                ratting_r=request.POST['rat']
            ).save()
    except KeyError:
        return JsonResponse({"error": "no post id provided in request"})

    return redirect(j.get_absolute_url())

def Add_Journal(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form=AddJournalForm(request.POST or None,request.FILES)
            if form.is_valid():
                instance=form.save(commit=False)
                instance.post_by=request.user
                instance.save()
                messages.add_message(request, messages.SUCCESS,
                                     'You have succesfully Add a Journal')
                if JournalPayment.objects.filter(jouenal_owner=request.user).exists():
                    pass
                else:
                    JournalPayment(
                        jouenal_owner=request.user,income=0
                    ).save()
                return redirect('addjournals')
        else:
            form=AddJournalForm()
        context={
            'form':form,
        }
        return render(request, 'journal/add_journal.html',context)


    else:
        return redirect('login')
def JournalManage(request):
    total_journal=Journal.objects.filter(post_by=request.user)
    sum=0
    acc=0
    paid=0
    rated=0
    for i in total_journal:
        sum=sum+i.download_count
    for i in total_journal:
        acc=acc+i.access.count()
    for i in total_journal:
        rated=rated+(i.no_of_rating())
    journal=Paginator(Journal.objects.all().filter(post_by=request.user).order_by('-id'),4)
    page = request.GET.get('page')
    try:
        posts = journal.page(page)
    except PageNotAnInteger:
        posts = journal.page(1)
    except EmptyPage:
        posts = journal.page(journal.num_pages)
    try:
        payment=JournalPayment.objects.get(jouenal_owner=request.user)
        paid=payment.income
    except:
        paid=0
    context={
        'all_journal':posts,
        'total_journal':total_journal,
        'total_download':sum,
        'total_access':acc,
        'total_income':paid,
        'total_rated':rated,
    }
    return render(request,'journal/manage_journal.html',context)

def DeleteJournal(request,id):
    journal=get_object_or_404(Journal,id=id)
    if request.user != journal.post_by:
        raise Http404()
    else:
        journal.delete()
        return redirect('managejournal')
def UpdateJournal(request,id):
    if request.user.is_authenticated:
        journal = get_object_or_404(Journal, id=id)
        if request.method=="POST":
            form = AddJournalForm(request.POST, request.FILES, instance=journal)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS,'You have succesfully updated your Journal')
                return redirect('managejournal')
        else:
            form = AddJournalForm(instance=journal)
        context = {
            'form': form,
        }

        return render(request,'journal/journalupdate.html',context)
    else:
        return redirect('login')

def ViewJournalInfo(request,id):
    journal = get_object_or_404(Journal, id=id)
    return render(request,'journal/viewjournalinfo.html',{'journal':journal})
def RequestPayment(request):
    if request.user.is_authenticated:
        if Journal.objects.filter(post_by=request.user).exists():
            total_journal = Journal.objects.filter(post_by=request.user)
            if total_journal:
                paid = 0
                acc = 0
                is_winthdraw = False
                for i in total_journal:
                    acc = acc + i.access.count()
                if JournalPayment.objects.filter(jouenal_owner=request.user).exists():
                    payment = JournalPayment.objects.get(jouenal_owner=request.user)
                    paid = payment.income
                    if paid >= 10:
                        is_winthdraw = True
                if request.method == "POST":
                    paypal_address = request.POST['paypal']
                    ammount = request.POST['ammount_']
                    RequestWithdraw.objects.create(
                        request_user=request.user,
                        paypal=paypal_address,
                        payment=ammount
                    ).save()
                    JournalPayment.objects.filter(jouenal_owner=request.user).update(income=F('income') - ammount)
                    mail_subject = 'Withdraw Request Confirmation'
                    message = render_to_string('journal/confirmwithdraw.html', {
                        'user': request.user,
                        'address': paypal_address,
                        'ammount': ammount,
                    })
                    to_email = request.user.email
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    messages.info(request, "your withdraw request is accepted")
                    return redirect('requestpayment')

                context = {
                    'total_income': paid,
                    'is_withdraw': is_winthdraw,
                }
                return render(request, 'journal/requestpayment.html', context)
            else:
                context = {
                    'total_income': 0,
                }
                return render(request, 'journal/requestpayment.html', context)
        else:
            is_winthdraw = False
            context = {
                'total_income': 0,
                'is_withdraw': is_winthdraw,
            }
            return render(request, 'journal/requestpayment.html', context)

    else:
        return redirect("login")

# def RequestPayment(request):
#     if request.user.is_authenticated:
#         total_journal = Journal.objects.filter(post_by=request.user)
#         if total_journal:
#             paid = 0
#             acc = 0
#             is_winthdraw = False
#             for i in total_journal:
#                 acc = acc + i.access.count()
#             payment = JournalPayment.objects.get(jouenal_owner=request.user)
#             paid = payment.income
#             if paid >= 50:
#                 is_winthdraw = True
#             if request.method == "POST":
#                 paypal_address = request.POST['paypal']
#                 ammount = request.POST['ammount_']
#                 RequestWithdraw.objects.create(
#                     request_user=request.user,
#                     paypal=paypal_address,
#                     payment=ammount
#                 ).save()
#                 JournalPayment.objects.filter(jouenal_owner=request.user).update(income=F('income') - ammount)
#                 mail_subject = 'Withdraw Request Confirmation'
#                 message = render_to_string('journal/confirmwithdraw.html', {
#                     'user': request.user,
#                     'address': paypal_address,
#                     'ammount': ammount,
#                 })
#                 to_email = request.user.email
#                 email = EmailMessage(
#                     mail_subject, message, to=[to_email]
#                 )
#                 email.send()
#                 messages.info(request, "your withdraw request is accepted")
#                 return redirect('requestpayment')
#
#             context = {
#                 'total_income': paid,
#                 'is_winthdraw': is_winthdraw,
#             }
#             return render(request, 'journal/requestpayment.html', context)
#         else:
#             context = {
#                 'total_income': 0,
#             }
#             return render(request, 'journal/requestpayment.html',context)
#
#     else:
#         return redirect("login")
