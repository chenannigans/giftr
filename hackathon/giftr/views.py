from django.shortcuts import render

# Create your views here.
def hello_world(request):
    # render takes: (1) the request,
    #               (2) the name of the view to generate, and
    #               (3) a dictionary of name-value pairs of data to be
    #                   available to the view template.
    return render(request, 'hello.html', {})
