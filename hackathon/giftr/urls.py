from django.conf.urls import include, url
from giftr.views import *
from django.contrib.auth import *

urlpatterns = [
	url(r'^$', gift_gallery, name='gift_gallery'),
	url(r'^login$', userlogin, name='userlogin'),
    url(r'^userlogin$', userlogin, name='userlogin'),
    url(r'^register$', register, name='register'),
    url(r'^gift_form$', gift_form, name = 'gift_form'),
    url(r'^upload_gift$', upload_gift, name='upload_gift'),
    url(r'^profile/(?P<who>[^/]+)/$', profile, name='profile'),
    url(r'^rewards/(?P<who>[^/]+)/$', rewards, name='rewards'),
    url(r'^gift/photo/(?P<id>\d+)$', get_photo, name='get_photo'),
	url(r'^gift/url/(?P<id>\d+)$', get_url, name='get_url'),
    url(r'^userlogout$', userlogout, name="userlogout"),
	url(r'^login_only$', login_only, name='login_only'),
    url(r'^search_gift/$', search_gift, name='search_gift'),
    url(r'^feeling_lucky/$', feeling_lucky, name='feeling_lucky'),
]
