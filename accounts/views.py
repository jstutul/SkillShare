import tempfile
from accounts.forms import UpdateOrgForm,UpdateReg,UpdateReg2
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.html import strip_tags
import requests
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core import files
from django.core.mail import EmailMessage
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from accounts.models import RegularUser,OrganizationUser
from mediablog.models import MediaBlog
# Create your views here.
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from io import BytesIO
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from accounts.tokens import account_activation_token
from mediablog.forms import MediaForm
from events.forms import EventForm
from events.models import EventManager
from scope.models import ScopeManage
from scope.forms import AddScopeForm
from ebook.forms import *

def  CreateR(user,city,phone,fb,photo,about):
    regular=RegularUser(user_r=user)
    regular.city=city
    regular.phone=phone
    regular.about_you=about
    regular.photo=photo
    regular.fb=fb
    regular.save()
def CreateO(user,city,phone,web,address,purpose,photo,org_name):
    organization = OrganizationUser(user_o=user)
    organization.city=city
    organization.phone=phone
    organization.fb=web
    organization.address=address
    organization.purpose=purpose
    organization.photo=photo
    organization.o_name=org_name
    organization.save()

def SIgnupView(request):
    return render(request,'user/signup.html')
def LoginView(request):
    if request.user.is_authenticated:
        return redirect('Mainhome')
    else:
        if request.method == 'POST':
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('Mainhome')
            else:
                messages.info(request,"Enter correct username and password")
                return redirect('login')

        else:
            return render(request, 'user/login.html')

def Logout_view(request):
    logout(request)
    return redirect('login')
def PasswordChange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'user/change_password.html', {
        'form': form
    })
def UpdateOrganization(request):
    if request.user.is_authenticated:
        userr=OrganizationUser.objects.get(user_o=request.user)
        if request.method=="POST":
            form = UpdateOrgForm(request.POST or None,request.FILES,instance=userr)
            if form.is_valid():
                form.save()
                messages.info(request, "your profile is updated !")
                return redirect('dashboard')
        else:
            form =UpdateOrgForm(instance=userr)
        return render(request,"user/updateorganization.html",{'form':form})

    else:
        return redirect('login')
def UpdateRegular(request):
    if request.user.is_authenticated:
        user1=RegularUser.objects.get(user_r=request.user)
        user2=User.objects.get(username=request.user)

        if request.method=="POST":
            form1 = UpdateReg(request.POST or None,request.FILES,instance=user1)
            form2 = UpdateReg2(request.POST or None,instance=user2)
            if form1.is_valid() and form2.is_valid():
                form1.save()
                form2.save()
                messages.info(request,"your profile is updated !")
                return redirect('dashboard')
        else:
            form1 =UpdateReg(instance=user1)
            form2 =UpdateReg2(instance=user2)
        return render(request,"user/updateregular.html",{'form1':form1,'form2':form2})

    else:
        return redirect('login')

def RegularView(request):
    if request.method=="POST":
        username=request.POST['username']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']
        comfirm_password=request.POST['comfirm_password']
        facebook=request.POST['facebook']
        city=request.POST['city']
        phone=request.POST['phone']
        about_you=request.POST['about_you']
        photo=request.FILES['photo']
        print(username,email,first_name,last_name,password,comfirm_password,city,facebook,phone,about_you,photo)
        if password==comfirm_password:
            if len(password)<8:
                messages.info(request, "password must be 8 character and strong")
                return redirect("signup")

            elif User.objects.filter(username=username).exists():
                messages.info(request, "user taken already")
                return redirect("signup")

            elif User.objects.filter(email=email).exists():
                messages.info(request, "email already taken")
                return redirect("signup")

            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email,
                                                password=password)
                user.is_active=False
                user.save()
                user.refresh_from_db()
                CreateR(get_object_or_404(User,username=username),city,phone,facebook,photo,about_you)
                current_site = get_current_site(request)
                mail_subject = 'Activate your  account.'
                message = render_to_string('user/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('<h1>Please confirm your email address to complete the registration and back to login</h1>')
        else:
            messages.info(request,"Password not matching")
            return redirect('signup')

    else:
        return redirect('signup')
def OrganizationView(request):
    if request.method=="POST":
        email=request.POST['org_email']
        password=request.POST['password']
        org_name=request.POST['org_name']
        comfirm_password=request.POST['comfirm_password']
        website=request.POST['website']
        city=request.POST['org_city']
        phone=request.POST['org_phone']
        address=request.POST['org_address']
        purpose = request.POST['purpose']
        photo=request.FILES['org_photo']
        if password==comfirm_password:
            if len(password)<8:
                messages.info(request, "password must be 8 character and strong")
                return redirect("signup")

            elif User.objects.filter(email=email).exists():
                messages.info(request, "email already taken")
                return redirect("signup")

            else:
                user = User.objects.create_user(username=email,email=email,password=password)
                user.is_active = False
                user.save()
                user.refresh_from_db()
                CreateO(get_object_or_404(User,username=email),city,phone,website,address,purpose,photo,org_name)
                current_site = get_current_site(request)
                mail_subject = 'Activate your  account.'
                message = render_to_string('user/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = email
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return HttpResponse('<h1>Please confirm your email address to complete the registration and back to login</h1>')
        else:
            messages.info(request,"Password not matching")
            return redirect('signup')

    else:
        return redirect('signup')
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('<h2>Thank you for your email confirmation. Now you can login your account.</h2>')
    else:
        return HttpResponse('Activation link is invalid!')
def Dashboard(request):
    if request.user.is_authenticated:
        is_user = False
        if RegularUser.objects.filter(user_r=request.user).exists():
            userr = RegularUser.objects.get(user_r=request.user)
            is_user = False
            context = {
                'is_user': is_user,
                'userr':userr
            }
            return render(request, 'dashboard/index.html', context)

        elif OrganizationUser.objects.filter(user_o=request.user).exists():
            userr = OrganizationUser.objects.get(user_o=request.user)
            is_user = True
            context = {
                'is_user': is_user,
                'userr': userr
            }
            return render(request, 'dashboard/index.html', context)

        context = {
            'is_user': is_user
        }
        return render(request, 'dashboard/index.html', context)
    else:
        return redirect('login')
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
    media.media_description=des
    media.thumbnail.save("thumbnail.jpg",files.File(lf))
def PostMedia(request):
    if request.user.is_authenticated:

        if request.method=="POST":
           form=MediaForm(request.POST or None,request.FILES)
           if form.is_valid():
               title=request.POST['title']
               link=request.POST['link']
               describtions=request.POST['media_description']
               CreateMedia(get_object_or_404(User, username=request.user), title, link, describtions)
               messages.info(request,"media saved succesfully")
               return redirect('postmedia')
        else:
            form=MediaForm()
        context={
            'form':form,
        }
        return render(request,'user/postmedia.html',context)
    else:
        return redirect('login')

def ViewMedia(request):
    media =MediaBlog.objects.filter(author=request.user)
    all_post =Paginator(MediaBlog.objects.filter(author=request.user).order_by('-id'),4)
    page = request.GET.get('page')
    try:
        posts =all_post.page(page)
    except PageNotAnInteger:
        posts = all_post.page(1)
    except EmptyPage:
        posts = all_post.page(all_post.num_pages)
    context ={
        'media':posts,
    }
    return render(request,'user/medialist.html',context)

def media_delete(request,id):
    posts = get_object_or_404(MediaBlog, id=id)
    if request.user != posts.author:
       raise Http404()
    posts.delete()
    return  redirect('viewmedia')
def Viewmediapost(request,id):
    post = get_object_or_404(MediaBlog, id=id)
    return render(request,'media/viewmediapost.html',{'post':post})

def Updatepost(request,id):
     posts = get_object_or_404(MediaBlog, id=id)
     if request.method=="POST":
         form = MediaForm(request.POST,request.FILES, instance=posts)
         if form.is_valid():
            post = form.save(commit=False)
            post.save()
            messages.add_message(request, messages.SUCCESS,
                                      'You have succesfully updated your post')
            return redirect('viewmedia')
     else:
         form=MediaForm(instance=posts)
     context={
             'form':form,
     }

     return render(request,'media/updatepost.html',context)


##Event part
def CreateEvent(title,user,cat,des,sd,ed,st,et,seat,fee,loc,reg,photo):
    event = EventManager(event_organizar=user)
    event.event_title=title
    event.category=cat
    event.description=des
    event.start_date=sd
    event.end_date=ed
    event.start_time=st
    event.end_time=et
    event.seat_limit=seat
    event.entry_fee=fee
    event.location=loc
    event.registration_link=reg
    event.banner=photo
    event.save()

def AddEvent(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            form=EventForm(request.POST or None ,request.FILES)
            if form.is_valid():
                event_title = request.POST.get("event_title")
                category = request.POST.get("category")
                description=request.POST.get("description")
                start_date = request.POST.get("start_date")
                end_date = request.POST.get("end_date")
                start_time = request.POST.get("start_time")
                end_time = request.POST.get("end_time")
                seat_limit = request.POST.get("seat_limit")
                entry_fee = request.POST.get("entry_fee")
                location = request.POST.get("location")
                registration_link = request.POST.get("registration_link")
                banner = request.FILES.get("banner")

                # instance=form.save(commit=False)
                # instance.event_organizar=request.user
                # instance.save()

                CreateEvent(event_title,get_object_or_404(User, username=request.user) , category, description, start_date, end_date, start_time, end_time, seat_limit, entry_fee,location, registration_link, banner)
                messages.info(request,"your event is saved succsesfuly")
                return redirect('addevent')
        else:
            form=EventForm()
        context={
            'form':form,
        }
        return render(request, 'user/postevent.html',context)
    else:
        return redirect('login')

def ViewEvent(request):
    all_post = Paginator(EventManager.objects.filter(event_organizar=request.user).order_by('-id'), 4)
    print(all_post)
    page = request.GET.get('page')
    try:
        posts = all_post.page(page)
    except PageNotAnInteger:
        posts = all_post.page(1)
    except EmptyPage:
        posts = all_post.page(all_post.num_pages)
    context = {
        'events': posts,
    }
    return render(request,'event/vieweventpost.html',context)

def Vieweventpost(request,id):
    event = get_object_or_404(EventManager, id=id)
    return render(request,'event/viewevent.html',{'event':event})


def Updateeventpost(request,id):
    if request.user.is_authenticated:
        event = get_object_or_404(EventManager, id=id)
        if request.method=="POST":
            form = EventForm(request.POST, request.FILES, instance=event)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS,'You have succesfully updated your post')
                return redirect('viewevent')
        else:
            form = EventForm(instance=event)
        context = {
            'form': form,
        }

        return render(request,'event/updateevent.html',context)
    else:
        return redirect('login')
def DeleteEvent(request,id):
    posts = get_object_or_404(EventManager, id=id)
    if request.user != posts.event_organizar:
        raise Http404()
    posts.delete()
    return redirect('viewevent')


def AddScope(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddScopeForm(request.POST or None, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                messages.info(request, "your scope is saved succsesfuly")
                return redirect('addscope')
        else:
            form = AddScopeForm()
        context = {
            'form': form,
        }
        return render(request,'scope/addscope.html',context)
    else:
        return redirect('login')
def VieweScope(request):
    all_post = Paginator(ScopeManage.objects.filter(user=request.user).order_by('-id'), 4)
    page = request.GET.get('page')
    try:
        posts = all_post.page(page)
    except PageNotAnInteger:
        posts = all_post.page(1)
    except EmptyPage:
        posts = all_post.page(all_post.num_pages)
    context = {
        'scope': posts,
    }
    return render(request,'scope/viewscope.html',context)

def VieweScopePost(request,id):
    scope = get_object_or_404(ScopeManage, id=id)
    if scope.user==request.user:
        context={
            'scope':scope,
        }
        return render(request,'scope/viewscopepost.html',context)
    else:
        raise Http404()

def EditScopePost(request,id):
    if request.user.is_authenticated:
        scope = get_object_or_404(ScopeManage, id=id)
        if scope.user==request.user:
            if request.method == "POST":
                form = AddScopeForm(request.POST, request.FILES, instance=scope)
                if form.is_valid():
                    form.save()
                    messages.add_message(request, messages.SUCCESS, 'You have succesfully updated your post')
                    return redirect('managescope')
            else:
                form = AddScopeForm(instance=scope)
            context = {
                'form': form,
            }

            return render(request, 'scope/updatescope.html', context)
        else:
            raise Http404()

    else:
        return redirect('login')


def DeleteScope(request,id):
    scope = get_object_or_404(ScopeManage, id=id)
    if request.user != scope.user:
        raise Http404()
    scope.delete()
    return redirect('managescope')

def AddBook(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = AddBookForm(request.POST or None, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.save()
                messages.info(request, "your Book is saved succsesfuly")
                return redirect('addbook')
        else:
            form = AddBookForm()
        context = {
            'form': form,
        }
        return render(request,'ebook/addbook.html',context)
    else:
        return HttpResponse("You are not eligible for this feature")
def ManageBook(request):
    if request.user.is_superuser:
        all_book = Paginator(Ebook.objects.all().order_by('-id'), 6)
        print(all_book)
        page = request.GET.get('page')
        try:
            posts = all_book.page(page)
        except PageNotAnInteger:
            posts = all_book.page(1)
        except EmptyPage:
            posts = all_book.page(all_book.num_pages)
        context = {
            'book': posts,
        }
        return render(request, 'ebook/viewbook.html', context)
    else:
        return HttpResponse("You are not eligible for this feature")
def EditBook(request,id):
    if request.user.is_superuser:
        book = get_object_or_404(Ebook, id=id)
        if request.method == "POST":
            form = AddBookForm(request.POST, request.FILES, instance=book)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'You have succesfully updated your post')
                return redirect('managebook')
        else:
            form = AddBookForm(instance=book)
        context = {
            'form': form,
        }

        return render(request, 'ebook/updatebook.html', context)
    else:
        return HttpResponse("You are not eligible for this feature")
def DeleteBook(request,id):
    if request.user.is_superuser:
        book = get_object_or_404(Ebook, id=id)
        book.delete()
        return redirect('managebook')
    else:
        return HttpResponse("You are not eligible for this feature")


