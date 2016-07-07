from django.conf.urls import include, url
from giftr.views import *

urlpatterns = [
	url(r'^$', gift_gallery, name='gift_gallery'),
	url(r'^login$', userlogin, name='userlogin'),

    # url(r'^populate$', populate, name='populate'),
    url(r'^register$', register, name='register'),
    url(r'^submit_form$', submit_form, name = 'submit_form'),
    url(r'^gift_form$', gift_form, name = 'gift_form'),
    url(r'^upload_gift$', upload_gift, name='upload_gift'),
]
