from django.shortcuts import render, redirect, get_object_or_404
from giftr.models import *
from giftr.forms import *
from giftr.getRewards import *
from django.core.urlresolvers import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse, Http404
from mimetypes import guess_type

import imghdr
import sys
# import getRewards
import subprocess

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import transaction
from itertools import islice, chain
from django.http import HttpResponse, Http404
from django.core.mail import send_mail
from .models import *
from .forms import *
from mimetypes import guess_type
from operator import attrgetter

from giftr.forms import *
from django.conf import settings

reward_balance = 5000.00
logged_in = False
customer = {}


@login_required
def gift_gallery(request):
    context = {}
    context['form'] = GiftForm()
    context['gifts'] = Gift.objects.all()
    context['user'] = request.user
    context['rewards_balance'] = reward_balance
    return render(request, 'gallery.html', context)


# @transaction.commit_on_success
@login_required
def upload_gift(request):
    if request.method == 'GET':
        form = GiftForm()
        return render(request, 'gallery.html', {'form': form})

    new_gift = Gift(user=request.user)
    form = GiftForm(request.POST, request.FILES, instance=new_gift)

    if not form.is_valid():
        form = GiftForm()
        return render(request, 'gallery.html', {'form': form})
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
        return render(request, 'register.html', {'form': form})

    form = RegisterForm(request.POST)
    if not form.is_valid():
        return render(request, 'register.html', {'form': form})
    else:
        user = User.objects.create_user(username=form.cleaned_data['username'], \
                                        password=form.cleaned_data['password1'], )
        user.save()
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
        login(request, user)
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

	# thing = request.POST['login']
	# print thing

	thing2 = request.POST['enter']
	if (thing2 == "login"):
		print "ENTERED HERE"
		return redirect(reverse('gift_gallery'))
	elif (thing2 == "cap-one"):
		print "ENTERED CAP ONE"
		return redirect('https://api-sandbox.capitalone.com/oauth/auz/authorize?redirect_uri=http://localhost:8000/giftr/cap-one-connect&scope=openid%20read_rewards_account_info&client_id=enterpriseapi-sb-0iSeXHHzheNu1AzI7DJbzea7&response_type=code')
	print thing2
	# print request.path
	# print request.get_full_path()

	# return redirect(reverse('gift_gallery'))



@login_required
def gift_form(request):
    form = GiftForm()
    return render(request, 'gallery.html', {'form': form})


@login_required
def profile(request, who):
    errors = []
    if not User.objects.filter(username=who).exists():
        return redirect(reverse('gift_gallery'))
    user = User.objects.filter(username=who)[0]
    gifts = Gift.objects.filter(user=user)
    context = {}
    context['user'] = user
    context['gifts'] = gifts
    context['rewards_balance'] = reward_balance
    context['logged_in'] = logged_in
    return render(request, 'profile.html', context)


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
    url = gift.url
    if not gift.url:
        url = "www.google.com/"
    if gift.url == "":
        url = "www.google.com/"
    content_type = guess_type(url)
    return redirect(gift.url, content_type=content_type)


@login_required
def search_gift(request):
    gift_str = request.GET['gift_str']
    gift_str.strip(" ")
    gift_strs = gift_str.split(",")
    gifts = []
    for s in gift_strs:
        s.strip(" ")

        gift = Gift.objects.filter(category__icontains=s)
        if not gift in gifts:
            gifts.extend(gift)

        gift = Gift.objects.filter(recipient_category__icontains=s)
        if not gift in gifts:
            gifts.extend(gift)

        gift = Gift.objects.filter(description__icontains=s)
        if not gift in gifts:
            gifts.extend(gift)

        if "price" in s:
            price = float(s[6:])
            LR = price - 10
            HR = price + 10
            gift = Gift.objects.filter(price__gte=LR, price__lte=HR)
            if not gift in gifts:
                gifts.extend(gift)

    context = {}
    context['form'] = GiftForm()
    context['gifts'] = gifts
    context['user'] = request.user
    context['rewards_balance'] = reward_balance
    context['logged_in'] = logged_in
    return render(request, 'gallery.html', context)


@login_required
def feeling_lucky(request):
    gift = Gift.objects.order_by('?').first()
    context = {}
    gifts = []
    gifts.append(gift)
    context['form'] = GiftForm()
    context['gifts'] = gifts
    context['user'] = request.user
    context['rewards_balance'] = reward_balance
    context['logged_in'] = logged_in
    return render(request, 'random.html', context)


@login_required
def rewards(request, who):
	errors = []
	if not User.objects.filter(username=who).exists():
		return redirect(reverse('gift_gallery'))
	user = User.objects.filter(username=who)[0]
	gifts = Gift.objects.filter(user=user)
	context={}
	context['user'] = user
	context['gifts'] = gifts
	context['rewards_balance'] = reward_balance
	context['logged_in'] = logged_in
	return render(request,'rewards.html', context)

@login_required
def cap_one_connect(request):
	print request.path
	print 'logged in to capital one account'
	print request.path
	print request.GET['code']
	code = request.GET['code']
	cards = get_cards(code)
	print vars(cards)
	return redirect(reverse('gift_gallery'))
