import tempfile
import json
from django.utils import timezone
from urllib.parse import quote_plus
import paginator as paginator
from django.contrib.auth.models import User
from django.db.models import F, Q
from mediablog.forms import *
from django.core.paginator import Paginator
from django.contrib.sites import requests
from django.core import files
from django.shortcuts import render, get_object_or_404,redirect
from mediablog.models import MediaBlog, Comment, Reaction
from django.template.loader import render_to_string
from django.http import JsonResponse
import datetime
from mediablog.forms import MediaForm

# Create your views here.
def MediaView(request):
    posts = MediaBlog.objects.all().order_by('-id')
    week_ago = datetime.date.today()-datetime.timedelta(days=30)
    trends = MediaBlog.objects.filter(post_on__gte=week_ago).order_by('-counter')[:10]
    comment =Comment.objects.all()
    query=request.GET.get('q')
    if query:
        posts=posts.filter(
            Q(title__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__username__icontains=query) |
            Q(author__mediablog__media_description__icontains=query)
        ).distinct()
    paginator =Paginator(posts,6)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'mediablog.html', {'posts':posts,'comment':comment,'trends':trends})
def DetailPost(request,id):
    if request.user.is_authenticated:
        post = get_object_or_404(MediaBlog,id=id)
        video_id = post.link.split('v=')[+1]
        popular=MediaBlog.objects.all().order_by('-counter')
        share_string=quote_plus(post.media_description)
        if post.view_counter.filter(id=request.user.id).exists():
            pass
        else:
            post.view_counter.add(request.user)
            post.count=F('counter')+1
        comments = Comment.objects.filter(post=post,reply=None).order_by('-id')
        if request.method=="POST":
            comment_form =CommentForm(request.POST or None)
            if comment_form.is_valid():
                content = comment_form.cleaned_data.get('content')
                reply_id = request.POST.get('comment_id')
                comment_qs = None
                if reply_id:
                    comment_qs = Comment.objects.get(id=reply_id)
                comment = Comment.objects.create(post=post,user=request.user,content=content,reply=comment_qs)
                comment.save()
                # return redirect(post.get_absolute_url())
        else:
            comment_form = CommentForm()
        context={
            'comments':comments,
            'post':post,
            'video_id':video_id,
            'comment_form':comment_form,
            'popular':popular[:5],
            'share_string':share_string,
        }
        if request.is_ajax():
            html = render_to_string('media/comment_section.html',context,request=request)
            return JsonResponse({'form':html})
        return render(request,'mediadetails.html',context)
    else:
        return redirect('login')


def react(request):
    # get user from request
    user = request.user
    # checking if it is an ajax request that was made
    if request.is_ajax:
        try:
            post_id = json.loads(request.body)['post_id']
            reaction_type = json.loads(request.body)['reactionType']
        except KeyError:
            return JsonResponse({"error": "no post id provided in request"})

        try:
            post = MediaBlog.objects.get(id=post_id)
        except MediaBlog.DoesNotExist:
            print("post not found")
            return JsonResponse({f'error': "no post with id {post_id}"})

        # has user reacted already
        try:
            reacted = post.reactions.get(user=user)
        except Reaction.DoesNotExist:
            reacted = None

        if reacted:
            # if user has already liked delete the reaction
            if reacted.reaction_type == reaction_type:
                reacted.delete()
                return JsonResponse({"status": "success", "action": {"decrease": reaction_type, "increase": None}})
            else:
                prev_reaction = reacted.reaction_type
                reacted.reaction_type = reaction_type
                reacted.save()
                return JsonResponse(
                    {"status": "success", "action": {"increase": reaction_type, "decrease": prev_reaction}})
        else:
            post.reactions.create(post=post, user=user, reaction_type=reaction_type)
            return JsonResponse(
                {"status": "success", "action": {"increase": reaction_type, "decrease": None}, post_id: "post.id"})
def CreateMedia(user,title,link,des):
    video_id = link.split('v=')[+1]
    thumbnail_url = f"http://img.youtube.com/vi/{video_id}/sddefault.jpg"
    request = requests.get(thumbnail_url,stream=True)

    lf = tempfile.NamedTemporaryFile()
    for block in request.iter_content(1024*8):
        if not block:
            break
        lf.write(block)
    media = MediaBlog(author=user)
    media.title=title
    media.link=link
    media.description=des
    media.thumbnail.save("thumbnail.jpg",files.File(lf))
