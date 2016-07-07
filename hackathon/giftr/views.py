from django.shortcuts import render, redirect
from giftr.models import *
from giftr.forms import * 
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, Http404
from mimetypes import guess_type

import imghdr

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
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

from giftr.forms import *
from django.conf import settings

@login_required
def gift_gallery(request):
	context = {}
	context['form'] = GiftForm()
	context['gifts'] = Gift.objects.all()
	context['user'] = request.user
	return render(request, 'gallery.html', context)

# @transaction.commit_on_success
@login_required
def upload_gift(request):
	if request.method == 'GET':
		form = GiftForm()
		return render(request, 'gallery.html', {'form':form})
	
	new_gift = Gift(user=request.user)
	form = GiftForm(request.POST, request.FILES, instance=new_gift)
	
	if not form.is_valid():
		form = GiftForm()
		return render(request, 'gallery.html', {'form':form})
	form.photo = form.cleaned_data['photo']
	form.save()
	return redirect(reverse('gift_gallery'))

# @transaction.commit_on_success
def register(request):
	if request.user.is_authenticated():
		return redirect(reverse('gift_gallery'))
	context = {}
	# Just display the registration form if this is a GET request
	if request.method == 'GET':
		form = RegisterForm()
		# context['form'] = RegisterForm()
		return render(request, 'register.html', {'form':form})

	form = RegisterForm(request.POST)
	if not form.is_valid():
		return render(request, 'register.html', {'form':form})
	else:
		user = User.objects.create_user(username=form.cleaned_data['username'], \
										password=form.cleaned_data['password1'],)
		user.save()
		user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
		login(request,user)
	return redirect(reverse('gift_gallery'))

def userlogin(request):
	errors = []
	if request.method == 'GET':
		errors.append("")
		context = {'errors':errors}
		return render(request, 'login.html', context)
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is None:
		errors.append("Invalid Password")
		context = {'errors':errors}
		return render(request,'login.html', context)	
	login(request, user)
	return redirect(reverse('gift_gallery'))

def login_only(request):
	errors = []
	if request.method == 'GET':
		errors.append("")
		context = {'errors':errors}
		return render(request, 'login_only.html', context)
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is None:
		errors.append("Invalid Password")
		context = {'errors':errors}
		return render(request,'login_only.html', context)
	login(request, user)
	return redirect(reverse('gift_gallery'))

@login_required
def gift_form(request):
	form = GiftForm()
	return render(request,'gallery.html', {'form':form})

@login_required
def profile(request, who):

	errors = []
	if not User.objects.filter(username=who).exists():
		return redirect(reverse('gift_gallery'))
	user = User.objects.filter(username=who)[0]
	gifts = Gift.objects.filter(user=user)
	context={}
	context['user'] = user
	context['gifts'] = gifts
	return render(request,'profile.html', context)

def userlogout(request):
	logout(request)
	return redirect(reverse('gift_gallery'))
	

@login_required
def get_photo(request, id):
	gift = Gift.objects.get(id=id)
	content_type = guess_type(gift.photo.name)
	return HttpResponse(gift.photo, content_type=content_type)

@login_required
def get_url(request, id):
	gift = Gift.objects.get(id=id)
	content_type = guess_type(gift.url)
	return redirect(gift.url, content_type=content_type)
	
# def get_photo(request, id):
# 	gift = Gift.objects.get(id=id)
# 	content_type = guess_type(gift.photo.name)
# 	print gift.photo.name
# 	return HttpResponse(gift.photo, content_type=content_type)
	

