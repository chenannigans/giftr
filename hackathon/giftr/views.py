from django.shortcuts import render, redirect
from giftr.models import *
from giftr.forms import * 
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction

from mimetypes import guess_type

from giftr.forms import *

# def loginpage(request):
# 	return render(request,'login.html', {})

# Create your views here.
# # @login_required
# def populate(request):
# 	g = Gift(picture = "pic", description = "desc", price = 5.20, url = "urlrulrur", category = "cat", recipient_category = "recicat", user_id = 1)
# 	g.save()
# 	return render(request,'populated.html', {'g':g})

@login_required
def gift_gallery(request):
	context = {}
	context['form'] = GiftForm()
	context['gifts'] = Gift.objects.all()
	return render(request, 'gallery.html', context)

# @transaction.commit_on_success
def upload_gift(request):
	if request.method == 'GET':
		form = GiftForm()
		return render(request, 'gallery.html', {'form':form})
	
	new_gift = Gift(user=request.user)
	form = GiftForm(request.POST, request.FILES, instance=new_gift)
	
	if not form.is_valid():
		form = GiftForm()
		print "INVALID FORM"
		return render(request, 'gallery.html', {'form':form})
	form.save()
	   
	print "SUCCESS UPLOAD"
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
		user = authenticate(username=username, password=password)
		login(request,user)
	return redirect(reverse('gift_gallery'))

def userlogin(request):
	print "HERE"
	errors = []
	if request.method == 'GET':
		print "getting render"
		errors.append("")
		context = {'errors':errors}
		return render(request, 'login.html', context)

	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username=username, password=password)
	if user is None:
		print "user not found"
		errors.append("Invalid Password")
		context = {'errors':errors}
		return render(request,'login.html', context)	
	login(request, user)
	print "success login"
	return redirect(reverse('gift_gallery'))

def gift_form(request):
	form = GiftForm()
	return render(request,'gallery.html', {'form':form})

def userlogout(request):
	logout(request)
	return redirect(reverse('gift_gallery'))


def profile(request, username):
	print 
	user =  User.objects.get(username=username)
	gifts = Gift.objects.filter(user=user)
	context={}
	context['user'] = user
	context['gifts'] = gifts
	return render(request,'profile.html', context)


