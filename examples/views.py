from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.db import transaction
from itertools import islice, chain
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from .models import *
from .forms import *
from mimetypes import guess_type
from operator import attrgetter
import imghdr

@login_required
def initial(request):
    form = PostForm()
    posts = Posts.objects.filter()
    requested_user=request.user
    username=requested_user.username
    context = {'posts': reversed(posts),'requested_user':username, 'form':form}
    return render(request, 'grumblr/grumblr_globalstream.html', context)

@login_required
def changepassword(request):
    user = User.objects.get(username=request.user)
    email = user.email
    return redirect(reverse('home'))

@login_required
def home(request):
    requested_user = request.user
    follow = Follow.objects.get(user=requested_user)
    follower_list = follow.following.all()
    matches = {}
    for s in follower_list:
        following_user = User.objects.get(username=s.username)
        p = Posts.objects.filter(user=following_user)
        matches = reversed(sorted(chain(matches,p),key=attrgetter('timestamp')))
    context= {'requested_user':requested_user,'following':follower_list, 'posts':matches}
    return render(request, 'grumblr/grumblr_home.html',context)

@login_required
def get_photo(request,who):
    find_user = User.objects.get(username=who)
    profile = get_object_or_404(Profile,user=find_user)
    if not profile.picture:
        # raise Http404
        content_type = guess_type(imghdr.what('photos/default.jpg'))
        return HttpResponse(open('photos/default.jpg'), content_type=content_type)
    content_type = guess_type(profile.picture.name)
    return HttpResponse(profile.picture, content_type=content_type)

@login_required
def editprofile(request):
    requested_user = request.user
    form = EditProfileForm(instance=request.user)
    profile = Profile.objects.get(user=requested_user)
    form2 = EditProfileForm2(instance=profile)
    if request.method == 'GET':
        context = {'form':form, 'form2':form2,'requested_user':requested_user}
        return render(request, 'grumblr/grumblr_editprofile.html',context)
    form = EditProfileForm(request.POST, instance=request.user)
    form2 = EditProfileForm2(request.POST,request.FILES, instance=profile)
    if not form.is_valid():
        context = {'form':form, 'form2':form2,'requested_user':requested_user}
        return render(request, 'grumblr/grumblr_editprofile.html',context)
    if not form2.is_valid():
        context = {'form':form, 'form2':form2,'requested_user':requested_user}
        return render(request, 'grumblr/grumblr_editprofile.html',context)
    form.save()
    form2.save()
    return redirect(reverse('home'))


@login_required
def follow(request,who):
    find_user = User.objects.get(username=who)
    requested_user = request.user
    follow = Follow.objects.get(user=requested_user)
    follow.following.add(find_user)
    return redirect(reverse('home'))

def unfollow(request,who):
    find_user = User.objects.get(username=who)
    requested_user = request.user
    follow = Follow.objects.get(user=requested_user)
    follow.following.remove(find_user)
    return redirect(reverse('home'))

@login_required
def addpost(request):
    form = PostForm(request.POST)
    if not form.is_valid():
        requested_user = request.user
        posts = Posts.objects.filter()
        context = {'posts' : reversed(posts),'requested_user':requested_user,'form':form}
        return render(request, 'grumblr/grumblr_globalstream.html', context)
    new_post=Posts(text=form.data['text'],user=request.user)
    new_post.save()
    requested_user = request.user
    posts = Posts.objects.filter()
    form = PostForm()
    context = {'posts' : reversed(posts),'requested_user':requested_user,'form':form}
    return render(request, 'grumblr/grumblr_globalstream.html', context)

@login_required
@transaction.atomic
def viewprofile(request, who):
    errors = []
    if not User.objects.filter(username=who).exists():
        errors.append('User does not exist')
        context={'errors':errors}
    else:
        find_user = User.objects.get(username=who)
        profile = Profile.objects.get(user=find_user)
        age = profile.age
        bio = profile.bio
        name=find_user.username
        requested_user = request.user
        posts = Posts.objects.filter(user=find_user)
        firstname = find_user.first_name
        lastname= find_user.last_name
        date = str(find_user.date_joined)[0:16]
        context = {'posts': reversed(posts),'name':name, 'firstname':firstname,'date':date,\
        'requested_user':requested_user,'lastname':lastname,'bio':bio,'age':age, 'errors':errors,'profile':find_user}
    return render(request, 'grumblr/grumblr_profile.html',context)

@transaction.atomic
def registration(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        context['form2'] = RegistrationForm2()
        return render(request, 'grumblr/grumblr_registration.html', context)
    form = RegistrationForm(request.POST)
    form2 = RegistrationForm2(request.POST,request.FILES)
    context['form']=form
    context['form2']=form2
    if not form.is_valid():
        return render(request, 'grumblr/grumblr_registration.html', context)
    new_user = User.objects.create_user(username=form.cleaned_data['username'], \
                                        email=form.cleaned_data['email'], \
                                        password=form.cleaned_data['password1'],\
                                        first_name=form.cleaned_data['first_name'],\
                                        last_name=form.cleaned_data['last_name'],
                                        )
    new_profile=Profile(bio=form.cleaned_data['bio'],age=form.cleaned_data['age'],user=new_user)
    form2 = EditProfileForm2(request.POST,request.FILES, instance=new_profile)
    new_profile.save()
    form2.save()
    new_user.save()
    new_user = authenticate(username=request.POST['username'], \
                            password=request.POST['password1'])
    new_followinglist=Follow(user=new_user)
    new_followinglist.save()
    login(request, new_user)
    return redirect(reverse('home'))
