from django.conf.urls import include, url
from giftr.views import *
from django.contrib.auth import *

urlpatterns = [
	url(r'^$', gift_gallery, name='gift_gallery'),
	url(r'^login$', userlogin, name='userlogin'),
    url(r'^register$', register, name='register'),
    url(r'^gift_form$', gift_form, name = 'gift_form'),
    url(r'^upload_gift$', upload_gift, name='upload_gift'),
    url(r'^(?P<who>\w+)$', profile, name='profile'),
    url(r'^userlogout$', userlogout, name='userlogout'),
    url(r'^gift/photo/(?P<id>\d+)$', get_photo, name='get_photo'),
    # url(r'^logout$', django.contrib.auth.views.logout_then_login),
]
