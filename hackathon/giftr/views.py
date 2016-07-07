from django.shortcuts import render
from giftr.models import *
from giftr.forms import * 

# Create your views here.
def hello_world(request):
	# render takes: (1) the request,
	#			   (2) the name of the view to generate, and
	#			   (3) a dictionary of name-value pairs of data to be
	#				   available to the view template.
	return render(request, 'hello.html', {})

def populate(request):
	g = Gift(picture = "pic", description = "desc", price = 5.20, url = "urlrulrur", category = "cat", recipient_category = "recicat", user_id = 1)
	g.save()
	return render(request,'populated.html', {'g':g})


def register(request):
	context = {}

	# Just display the registration form if this is a GET request
	if request.method == 'GET':
		# form = RegisterForm()
		form = RegisterForm()
		# context['form'] = RegisterForm()
		return render(request, 'register.html', {'form':form})

	errors = []
	context['errors'] = errors

	form = RegisterForm(request.POST)
	if form.is_valid():
		return render(request, 'hello.html', {})
	else:
		form = RegisterForm()

	return render(request,'register.html', {'form':form})

# def login(request):
# 	context = {}

# 	# Just display the registration form if this is a GET request
# 	if request.method == 'GET':
# 		return render(request, 'register.html', context)

# 	errors = []
# 	context['errors'] = errors

# 	# Checks the validity of the form data
# 	if not 'username' in request.POST or not request.POST['username']:
# 		errors.append('Username is required.')
# 	else:
# 		# Save the username in the request context to re-fill the username
# 		# field in case the form has errrors
# 	context['username'] = request.POST['username']

# 	if not 'password' in request.POST or not request.POST['password']:
# 	errors.append('Password is required.')

# 	if errors:
# 		return render(request, 'register.html', context)

# 	# Creates the new user from the valid form data
# 	new_user = User.objects.create_user(username=request.POST['username'], \
# 										password=request.POST['password1'])
# 	new_user.save()

# 	# Logs in the new user and redirects to his/her todo list
# 	new_user = authenticate(username=request.POST['username'], \
# 							password=request.POST['password'])
# 	login(request, new_user)
# 	return redirect('/giftr/')
