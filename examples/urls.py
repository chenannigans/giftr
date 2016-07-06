from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import *

urlpatterns = [
    url(r'^$', 'grumblr.views.initial', name='initial'),
    url(r'^globalstream', 'grumblr.views.initial', name='globalstream'),
    url(r'^home','grumblr.views.home',name='home'),
    url(r'^registration', 'grumblr.views.registration', name='registration'),
    url(r'^addpost', 'grumblr.views.addpost',name='addpost'),
    url(r'^login', 'django.contrib.auth.views.login', {'template_name':'grumblr/grumblr_login.html'}, name='login'),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login',name='logout'),
    url(r'^profile/(?P<who>[^/]+)/$', 'grumblr.views.viewprofile',name='viewprofile'),
    url(r'^follow/(?P<who>[^/]+)/$', 'grumblr.views.follow',name='follow'),
    url(r'^unfollow/(?P<who>[^/]+)/$', 'grumblr.views.unfollow',name='unfollow'),
    url(r'^editprofile', 'grumblr.views.editprofile',name='editprofile'),
    url(r'^photo/(?P<who>[^/]+)/$', 'grumblr.views.get_photo',name='photo'),
    url(r'^changepassword', 'grumblr.views.changepassword',name='changepassword'),
]
