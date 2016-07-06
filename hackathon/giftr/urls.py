from django.conf.urls import include, url

urlpatterns = [
	url(r'^$', 'giftr.views.hello_world'),
    url(r'^hello-world$', 'giftr.views.hello_world'),
<<<<<<< HEAD
    url(r'^make$', 'giftr.views.make'),
    # url(r'^hello.html$', 'intro.views.hello'),
=======
    url(r'^populate$', 'giftr.views.populate'),
>>>>>>> ea5d1b1d4f0ae2fb5b24e62a517e34f33ac4ccff
]
