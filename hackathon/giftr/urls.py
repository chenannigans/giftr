from django.conf.urls import include, url
from giftr.views import *

urlpatterns = [
	url(r'^$', hello_world, name='hello_world'),
    url(r'^hello-world$', hello_world),
    # url(r'^make$', make, name='make'),
    # url(r'^hello.html$', 'intro.hello'),
    url(r'^populate$', populate, name='populate'),
    url(r'^register$', register, name='register'),
]
