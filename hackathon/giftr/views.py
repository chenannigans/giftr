from django.shortcuts import render
from giftr.models import *

# Create your views here.
def hello_world(request):
    # render takes: (1) the request,
    #               (2) the name of the view to generate, and
    #               (3) a dictionary of name-value pairs of data to be
    #                   available to the view template.
    return render(request, 'hello.html', {})

def populate(request):
	g = Gift(picture = "pic", description = "desc", price = 5.20, url = "urlrulrur", category = "cat", recipient_category = "recicat", user_id = 1)
	g.save()
	return render(request,'populated.html', {'g':g})