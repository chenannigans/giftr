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
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.mail import send_mail  
from .models import *
from .forms import *
from mimetypes import guess_type
from operator import attrgetter

from giftr.forms import *
from django.conf import settings

global cash_balance
global cards
customer = {}
logged_in = False
connected = True
global cards
test = ['a','b','c']

@login_required
def gift_gallery(request):
    global cash_balance
    global cards
    global connected
    context = {}
    context['form'] = GiftForm()
    context['gifts'] = Gift.objects.all()
    context['user'] = request.user
    context['connection'] = connected
    connected = True
    try:
        context['rewards_balance'] = cash_balance
    except NameError:
        context['rewards_balance'] = None
    try:
        context['cards'] = cards
    except NameError:
        context['cards'] = None
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
    global cards
    errors = []
    if not User.objects.filter(username=who).exists():
        return redirect(reverse('gift_gallery'))
    user = User.objects.filter(username=who)[0]
    gifts = Gift.objects.filter(user=user)
    context = {}
    context['user'] = user
    context['gifts'] = gifts
    try:
        context['rewards_balance'] = cash_balance
    except NameError:
        context['rewards_balance'] = None
    try:
        context['cards'] = cards
    except NameError:
        context['cards'] = None
    context['logged_in'] = logged_in
    context['connection'] = connected
    context['profile']=True
    
    return render(request, 'profile.html', context)


def userlogout(request):
    global cash_balance
    global cards
    cards = None
    cash_balance = None
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
    global cards
    gift_str = request.GET['gift_str']
    # gift_str.strip(" ")
    gift_strs = gift_str.split(",")
    gift_strs = gift_str.split(" ")
    gifts = []
    price = None
    for s in gift_strs:
        if s.isdigit():
            price = int(s)
            LR = price - 10
            HR = price + 10
            if len(gift_strs)==1:
                print "ONLY ONE"
                gift = Gift.objects.filter(price__gte=LR, price__lte=HR)
                gifts.extend(gift)

    for s in gift_strs:
        # s.strip(" ")
        if price is not None:
            gift = Gift.objects.filter(category__icontains=s, price__gte=LR, price__lte=HR)
        else:
            gift = Gift.objects.filter(category__icontains=s)
        gifts.extend(gift)

        if price is not None:
            gift = Gift.objects.filter(recipient_category__icontains=s, price__gte=LR, price__lte=HR)
        else:
            gift = Gift.objects.filter(recipient_category__icontains=s)
        gifts.extend(gift)

        if price is not None:
            gift = Gift.objects.filter(description__icontains=s, price__gte=LR, price__lte=HR)
        else:
            gift = Gift.objects.filter(description__icontains=s)
        gifts.extend(gift)

    gifts = list(set(gifts))
    context = {}
    context['form'] = GiftForm()
    context['gifts'] = gifts
    context['user'] = request.user
    context['connection'] = connected
    try:
        context['rewards_balance'] = cash_balance
    except NameError:
        context['rewards_balance'] = None
    try:
        context['cards'] = cards
    except NameError:
        context['cards'] = None
    context['logged_in'] = logged_in
    return render(request, 'gallery.html', context)


@login_required
def feeling_lucky(request):
    global cards
    gift = Gift.objects.order_by('?').first()
    context = {}
    gifts = []
    gifts.append(gift)
    context['form'] = GiftForm()
    context['gifts'] = gifts
    context['user'] = request.user
    try:
        context['rewards_balance'] = cash_balance
    except NameError:
        context['rewards_balance'] = None
    try:
        context['cards'] = cards
    except NameError:
        context['cards'] = None
    context['logged_in'] = logged_in
    context['connection'] = connected
    return render(request, 'random.html', context)


@login_required
def rewards(request, who):
    global cards
    errors = []
    if not User.objects.filter(username=who).exists():
        return redirect(reverse('gift_gallery'))
    user = User.objects.filter(username=who)[0]
    gifts = Gift.objects.filter(user=user)
    context={}
    context['user'] = user
    context['gifts'] = gifts
    try:
        context['rewards_balance'] = cash_balance
    except NameError:
        context['rewards_balance'] = None
    try:
        context['cards'] = cards
    except NameError:
        context['cards'] = None
    context['logged_in'] = logged_in
    return render(request,'rewards.html', context)

@login_required
def cap_one_connect(request):
    global cards
    global cash_balance
    global connected
    print request.path
    print 'logged in to capital one account'
    print request.path
    print request.GET['code']
    code = request.GET['code']
    try:
        cash_balance, cards = get_cash_balance(code)
        return redirect(reverse('gift_gallery'))
    except:
        connected = False
        return redirect(reverse('gift_gallery'))


@login_required
def delete_post(request, id):
    query = Gift.objects.get(id=id)
    query.delete()

    return HttpResponseRedirect('/giftr/')
