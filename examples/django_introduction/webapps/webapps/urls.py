from django.conf.urls import include, url

urlpatterns = [
    url(r'^intro/', include('intro.urls')),
]
