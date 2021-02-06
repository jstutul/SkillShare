from django.http import Http404
from django.shortcuts import render,redirect,get_object_or_404
from community.models import *
from django.contrib import messages
from django.db.models import F, Q
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
def CommunityHome(request):
    if request.user.is_authenticated:
        blog=Blog.objects.all().order_by('-id')
        comments = BlogComment.objects.all()
        subcomment = SubComment.objects.all()
        query=request.GET.get('q')
        if query:
            blog=blog.filter(
                Q(title__icontains=query) |
                Q(author__first_name__icontains=query) |
                Q(author__username__icontains=query)
            ).distinct()
        if request.method == 'POST':
            comm =request.POST.get('comm')
            comm_id =request.POST.get('comm_id')
            post_id =request.POST.get('post_id')
            post = Blog.objects.get(id=post_id)
            if comm =="":
                pass
            else:
                if comm_id:
                    SubComment(
                            post=post,
                            user=request.user,
                            content = comm,
                            comment =BlogComment.objects.get(id=comm_id)
                    ).save()
                else:
                    BlogComment(
                        post=post,
                        user=request.user,
                        content=comm,
                    ).save()
                    return redirect("communityhome")
        context = {
        'subcomment':subcomment,
        'comments':comments,
        'blog':blog,
        }
        return render(request,'community/community.html',context)
    else:
        return redirect('login')
def AddPost(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user=request.user
            title=request.POST.get('titlec')
            des=request.POST.get('desc')
            Blog(
            author=user,title=title,details=des
            ).save()
            messages.info(request,"Post added succesfully !")
            return redirect('addcommunity')
        else:
            return render(request,'community/addcommunity.html')
    else:
        return redirect('login')

def ManageC(request):
    if request.user.is_authenticated:
        all_post =Paginator(Blog.objects.filter(author=request.user).order_by('-id'),4)
        page = request.GET.get('page')
        try:
            posts =all_post.page(page)
        except PageNotAnInteger:
            posts = all_post.page(1)
        except EmptyPage:
            posts = all_post.page(all_post.num_pages)
        context ={
        'community':posts,
        }
        return render(request,'community/managecommunity.html',context)
    else:
        return redirect('login')
def DeleteC(request,id):
    posts = get_object_or_404(Blog, id=id)
    if request.user != posts.author:
       raise Http404()
    posts.delete()
    return  redirect('managec')
def UpdateC(request,id):
     post = get_object_or_404(Blog, id=id)
     if request.method=="POST":
         title=request.POST.get('titlec')
         des=request.POST.get('desc')
         post.title=title
         post.details=des
         post.save()
         messages.add_message(request, messages.SUCCESS,'You have succesfully updated your post')
         return redirect('managec')
     else:
         pass
def ViewC(request,id):
    if request.user.is_authenticated:
        post = Blog.objects.get(id=id)
        context ={
        'post':post,
        }
        return render(request,'community/Viewcommunity.html',context)
    else:
        return redirect('login')
