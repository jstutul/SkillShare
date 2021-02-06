import datetime
from urllib.parse import quote_plus

from django.db.models import F, Q
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from events.models import EventManager,EventComment
from events.forms import CommentForm
from django.core.paginator import Paginator
# Create your views here.
def EventHome(request):
    events =EventManager.objects.all().order_by('-id').filter(end_date__gte=datetime.date.today())

    trends = EventManager.objects.all().order_by('-id').filter(end_date__gte=datetime.date.today()).order_by('-view_count')[:10]
    query = request.GET.get('q')
    if query:
        events = events.filter(
            Q(event_title__icontains=query) |
            Q(category__icontains=query) |
            Q(event_organizar__username__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
    paginator = Paginator(events, 6)
    page = request.GET.get('page')
    events = paginator.get_page(page)

    context ={
        'events':events,
        'trends':trends,
    }
    return render(request,'event/events.html',context)

def DetailsEvent(request,category,id):
    if request.user.is_authenticated:
        event = get_object_or_404(EventManager, id=id)
        share_string = quote_plus(event.description)
        if event.event_view.filter(id=request.user.id).exists():
            pass
        else:
            event.event_view.add(request.user)
            EventManager.objects.filter(id=id).update(view_count=F('view_count')+1)
        event=get_object_or_404(EventManager,id=id)
        popular_event=EventManager.objects.all().order_by('-view_count')[:7]
        share_link=quote_plus(event.description)
        is_interested = False
        if event.interested.filter(id=request.user.id).exists():
            is_interested=True
        comments = EventComment.objects.filter(post=event, reply=None).order_by('-id')
        if request.method=="POST":
            comment_form =CommentForm(request.POST or None)
            if comment_form.is_valid():
                content = comment_form.cleaned_data.get('content')
                reply_id = request.POST.get('comment_id')
                comment_qs = None
                if reply_id:
                    comment_qs = EventComment.objects.get(id=reply_id)
                comment = EventComment.objects.create(post=event,user=request.user,content=content,reply=comment_qs)
                comment.save()
                # return redirect(event.get_absolute_url())
        else:
            comment_form = CommentForm()
        context={
            'event':event,
            'comments': comments,
            'comment_form': comment_form,
            'share_link':share_link,
            'is_interested':is_interested,
            'total_interested':event.total_interested(),
            'popular_event':popular_event,
            'share_string': share_string,
        }
        if request.is_ajax():
            html = render_to_string('event/comment_section.html',context,request=request)
            return JsonResponse({'form':html})
        return render(request, 'event/evetdetails.html',context)


    else:
        return redirect('login')

def interested_event(request):
    event=get_object_or_404(EventManager,id=request.POST.get('event_id'))
    is_interested=False
    if event.interested.filter(id=request.user.id).exists():
        event.interested.remove(request.user)
        is_interested=False
    else:
        event.interested.add(request.user)
        is_interested=True

    context = {
        'event': event,
        'is_interested': is_interested,
        'total_interested': event.total_interested(),
    }
    if request.is_ajax():
        html=render_to_string('event/interested_section.html',context,request=request)
        return JsonResponse({'form':html})
