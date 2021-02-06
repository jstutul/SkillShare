import datetime
from django.core.paginator import Paginator
from django.db.models import F, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
import json
from scope.models import ScopeManage, ScopeComment
from scope.forms import CommentForm
from urllib.parse import quote_plus
# Create your views here.
def ScopeHome(request):
    scope=ScopeManage.objects.all().order_by('-id').filter(end_date__gte=datetime.date.today())
    trends = ScopeManage.objects.all().order_by('-id').filter(end_date__gte=datetime.date.today()).order_by(
        '-scope_counter')[:8]

    query=request.GET.get('q')
    if query:
        scope=scope.filter(
            Q(scope_title__icontains=query) |
            Q(details__icontains=query) |
            Q(category__icontains=query)
        ).distinct()
    paginator = Paginator(scope, 6)
    page = request.GET.get('page')
    scope = paginator.get_page(page)
    context={
        'scope':scope,
        'trends':trends,
    }
    return render(request,'scope/scopehome.html',context)

def ScopeView(request,category,id):
    if request.user.is_authenticated:
        scope=get_object_or_404(ScopeManage,id=id)
        share_string = quote_plus(scope.details)
        if scope.scope_viewer.filter(id=request.user.id).exists():
            pass
        else:
            scope.scope_viewer.add(request.user)
            ScopeManage.objects.filter(id=id).update(scope_counter=F('scope_counter') + 1)
        scope = get_object_or_404(ScopeManage, id=id)
        popular_scope = ScopeManage.objects.all().order_by('-scope_counter')[:7]
        comments = ScopeComment.objects.filter(post=scope, reply=None).order_by('-id')
        if request.method=="POST":
            comment_form =CommentForm(request.POST or None)
            if comment_form.is_valid():
                content = comment_form.cleaned_data.get('content')
                reply_id = request.POST.get('comment_id')
                comment_qs = None
                if reply_id:
                    comment_qs = ScopeComment.objects.get(id=reply_id)
                comment = ScopeComment.objects.create(post=scope,user=request.user,content=content,reply=comment_qs)
                comment.save()

        else:
            comment_form = CommentForm()

        is_liked = False
        is_loved = False
        if scope.reactions.filter(id=request.user.id).exists():
            is_liked = True
        if scope.love.filter(id=request.user.id).exists():
            is_loved=True
        context={
            'scope':scope,
            'popular_scope':popular_scope,
            'is_liked':is_liked,
            'is_loved':is_loved,
            'comments': comments,
            'comment_form': comment_form,
            'share_string': share_string,
        }
        if request.is_ajax():
            html = render_to_string('scope/comment_section.html', context, request=request)
            return JsonResponse({'form': html})
        return render(request,'scope/scopedetails.html',context)
    else:
        return redirect('login')

def scope_like(request):
    scope = get_object_or_404(ScopeManage, id=request.POST.get('scope_id'))
    is_liked = False
    is_loved=False
    if scope.reactions.filter(id=request.user.id).exists():
        scope.reactions.remove(request.user)
        is_liked = False

    else:
        if scope.love.filter(id=request.user.id).exists():
            scope.love.remove(request.user)
            is_loved=False
        scope.reactions.add(request.user)
        is_liked = True

    context = {
        'scope': scope,
        'is_liked': is_liked,
        'is_loved':is_loved,
        'total_like': scope.total_reactions(),
    }
    if request.is_ajax():
        html = render_to_string('scope/reaction_section.html', context, request=request)
        return JsonResponse({'form': html})
def scope_love(request):
    scope = get_object_or_404(ScopeManage, id=request.POST.get('scope_id'))
    is_loved = False
    is_liked=False
    if scope.love.filter(id=request.user.id).exists():
        scope.love.remove(request.user)
        is_loved = False
    else:
        if scope.reactions.filter(id=request.user.id).exists():
            scope.reactions.remove(request.user)
            is_liked=False
        scope.love.add(request.user)
        is_loved = True

    context = {
        'scope': scope,
        'is_loved': is_loved,
        'is_liked':is_liked,
        'total_love': scope.total_love(),
    }
    if request.is_ajax():
        html = render_to_string('scope/reaction_section.html', context, request=request)
        return JsonResponse({'form': html})
