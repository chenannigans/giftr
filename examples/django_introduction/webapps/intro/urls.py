from django.conf.urls import include, url

urlpatterns = [
    url(r'^hello-world$', 'intro.views.hello_world'),
    url(r'^hello.html$', 'intro.views.hello'),
]
