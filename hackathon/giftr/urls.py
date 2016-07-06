from django.conf.urls import include, url

urlpatterns = [
	url(r'^$', 'giftr.views.hello_world'),
    url(r'^hello-world$', 'giftr.views.hello_world'),
    url(r'^make$', 'giftr.views.make'),
    # url(r'^hello.html$', 'intro.views.hello'),
]
