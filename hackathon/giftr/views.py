from django.shortcuts import render, redirect
from giftr.models import *
from giftr.forms import * 
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from giftr.forms import *

# def loginpage(request):
# 	return render(request,'login.html', {})

# Create your views here.
# # @login_required
# def populate(request):
# 	g = Gift(picture = "pic", description = "desc", price = 5.20, url = "urlrulrur", category = "cat", recipient_category = "recicat", user_id = 1)
# 	g.save()
# 	return render(request,'populated.html', {'g':g})

# @login_required
def hello_world(request):
	# render takes: (1) the request,
	#			   (2) the name of the view to generate, and
	#			   (3) a dictionary of name-value pairs of data to be
	#				   available to the view template.
	return render(request, 'hello.html', {})

# @login_required
def gift_gallery(request):
	context = {}
	context['form'] = GiftForm()
	context['gifts'] = Gift.objects.all()
	return render(request, 'gallery.html', context)

def upload_gift(request):
	if request.method == 'GET':
		form = GiftForm()
		return render(request, 'gallery.html', {'form':form})
	
	form = GiftForm(request.POST)
	
	if not form.is_valid():
		form = GiftForm()
		return redirect(reverse('gift_gallery'))
	form.save()
	return redirect(reverse('gift_gallery'))

def register(request):
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
		login(request,user)
	return redirect(reverse('hello_world'))

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
	return redirect(reverse('hello_world'))

def gift_form(request):
	form = GiftForm()
	return render(request,'gallery.html', {'form':form})

def submit_form(request):
	print "alsknda"
	return render(request, 'hello.html', {})
