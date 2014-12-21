from django.shortcuts import render, redirect
from django.forms import ValidationError
from django.db import IntegrityError
from users import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from users.models import UserProfile, Message

# form view for creating a new user
def signup(request):
	title = 'Sign up for ToolShare!'
	
	if request.method == 'GET':
		form = forms.SignUpForm()
	else:
		form = forms.SignUpForm(request.POST)
	
		if form.is_valid():	
			# tries to create an user from the information provided. Displays any error that may appear
			try:
				username, password = form.save()
			# a ValidationError is thrown if the zip code contains non-numeral characters OR the passwords do not match
			except ValidationError as e:
				message = e.message
				return render(request, 'signup.html', {'title': title, 'message': message, 'form': form})
			# a IntegrityError is thrown if the unique constraint in the model is violated
			except IntegrityError as e:
				message = 'A user with this username already exists. Please choose another username.'
				return render(request, 'signup.html', {'title': title, 'message': message, 'form': form})

			# signs in the new user and redirects to the create/join community form view
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('join_community')
	
	message = 'Please fill in the information below.'
	return render(request, 'signup.html', {'title': title, 'message': message, 'form': form})

# form view for joining/creating a community, displays directly after the sign up form
@login_required
def join_community(request):
	title = 'Join or Create a Community!'
	
	if request.method == 'GET':
		form = forms.JoinCommunityForm(request)
	else:
		form = forms.JoinCommunityForm(request, request.POST)
		
		if form.is_valid():
			# sets the community in the user's model instance (and creates it if it doesn't exist in the community database)
			form.set(request)
			request.session['message'] = 'Community successfully joined! Welcome to ToolShare!'
			return redirect('profile')
	
	message = 'Just one more thing. Please select a community to join (or create a new one)!'
	return render(request, 'form.html', {'title': title, 'message': message, 'form': form})
	
# form view for signing in a user
def signin(request):
	title = 'Sign in to ToolShare!'
	
	if request.method == 'GET':
		form = forms.SignInForm()
	else:
		form = forms.SignInForm(request.POST)
		
		if form.is_valid():
			# authenticates the user
			username, password = form.get()
			user = authenticate(username=username, password=password)
			
			# checks if the user is active, and signs the user in
			if user is not None:
				if user.is_active:
					login(request, user)
					request.session['message'] = 'You have signed in successfully!'
					return redirect('profile')
			# if authentication fails or the user is not active, display an error message
				else:
					message = 'Incorrect username or password. Please try again.'
			else:
				message = 'Incorrect username or password. Please try again.'
				
			return render(request, 'signin.html', {'title': title, 'message': message, 'form': form})
										
	message = 'Enter your username and password.'
	return render(request, 'signin.html', {'title': title, 'message': message, 'form': form})

# view to sign a user out. Simply signs out the user in the authentication system and redirects to the index page
@login_required
def signout(request):
	logout(request)
	return redirect('index')
	
# view for the user's profile page
@login_required
def profile(request):
	# a number of views redirects here. Display a appropriate success message from that view
	try:
		message = request.session['message']
		del request.session['message']
	# if there was no redirect, display a appropriate welcome message
	except KeyError:
		message = 'Welcome to your profile page!'
	
	# obtains the user's information and pass it to the template for display
	username = request.user.username
	user = UserProfile.objects.get(user=User.objects.get(username=username))
	user_info = user.get_profile_info()
	zipcode = user_info['Zip Code'].split()[0][:]
	return render(request, 'profile.html', {'username': username, 'message': message, 'user_info': user_info, 'zipcode': zipcode, 'pickup_arrangement': user_info['Pickup Arrangement']})

# view for changing the user's name
@login_required		
def change_name(request):
	title = 'Change Your Name'
	
	if request.method == 'GET':
		form = forms.ChangeNameForm()
	else:
		form = forms.ChangeNameForm(request.POST)
		
		if form.is_valid():
			# changes the name in the user's model instance and redirects to the profile view with a success message
			form.change_name(request)
			request.session['message'] = 'Your name successfully updated!'
			return redirect('profile')
		
	message = 'Fill out the form below to change your name.'
	return render(request, 'change_name.html', {'title': title, 'message': message, 'form': form})

# view for changing the user's zip code
@login_required
def change_zip_code(request):
	title = 'Change Your Zip Code'
	
	if request.method == 'GET':
		form = forms.ChangeZipCodeForm()
	else:
		form = forms.ChangeZipCodeForm(request.POST)
		
		if form.is_valid():
			# changes the user's zip code
			try:
				form.change_zip_code(request)
			# a ValidationError is thrown if the zip code contains non-numeral characters
			except ValidationError as e:
				message = e.message
				return render(request, 'form.html', {'title': title, 'message': message, 'form': form})
			
			# if successful, redirects to the join community view so the user can pick a new community to join, or create a new one
			return redirect('join_community')
					
	message = 'Fill out the form below to change your zip code and move to your new local ToolShare community!'
	return render(request, 'change_zipcode.html', {'title': title, 'message': message, 'form': form})
	
# view for updating the user's pickup arrangements
@login_required
def change_pickup_arrangement(request):
	title = 'Change Your Pickup Arrangement'
	
	if request.method == 'GET':
		form = forms.UpdatePickupArrangementForm()
	else:
		form = forms.UpdatePickupArrangementForm(request.POST)
		
		if form.is_valid():
			# changes the pickup arrangements in the user's model instance and redirects to the profile with a success message
			form.change_pickup_arrangement(request)
			request.session['message'] = 'Your pickup arrangement successfully updated!'
			return redirect('profile')	
		
	message = 'Tell us anything we should know about the pickup arrangements for your tools!'
	return render(request, 'change_pickup.html', {'title': title, 'message': message, 'form': form})

# view to change the user's password
@login_required	
def change_password(request):
	title = 'Change Your Password'
	
	if request.method == 'GET':
		form = forms.ChangePasswordForm()
	else:
		form = forms.ChangePasswordForm(request.POST)
		
		if form.is_valid():
			try:
				current_password, new_password = form.get(request)
			# a ValidationError is thrown if the passwords do not match
			except ValidationError as e:
				message = e.message
				return render(request, 'form.html', {'title': title, 'message': message, 'form': form})
			
			user = authenticate(username=request.user.username, password=current_password)
			
			# if authentication is successful, change the password and redirects to the profile with a success message
			if user is not None:
				user.set_password(new_password)
				user.save()
				request.session['message'] = 'Your password successfully changed!'
				return redirect('profile')
			# if authentication fails, display an error message
			else:
				message = 'Incorrect password.'
				return render(request, 'form.html', {'title': title, 'message': message, 'form': form})
						
	message = 'Fill out the form below to change your password.'
	return render(request, 'change_password.html', {'title': title, 'message': message, 'form': form})

# view to delete the user's account
@login_required	
def delete_account(request):
	title = 'Delete Your Account'
	
	if request.method == 'GET':
		form = forms.DeleteAccountForm()
	else:
		form = forms.DeleteAccountForm(request.POST)
		
		if form.is_valid():
			# authenticates the user
			password = form.get()
			user = authenticate(username=request.user.username, password=password)
			
			# upon sucessful authentication, sets the is_active flag to false and redirects to the index page
			if user is not None:
				request.user.is_active = False
				request.user.save()
				logout(request)
				return redirect('index')
			# else if authentication fails, display appropriate error message
			else:
				message = 'Incorrect password.'
				return render(request, 'form.html', {'title': title, 'message': message, 'form': form})
						
	message = 'Are you absolutely sure you want to delete your account? If you are, please type your password and tick the checkbox below and click submit.'
	return render(request, 'delete_account.html', {'title': title, 'message': message, 'form': form})

# form view for composing a message to another user
@login_required	
def send_message(request):
	title = 'Message a User'
	
	if request.method == 'GET':
		form = forms.MessageForm(request)
	else:
		form = forms.MessageForm(request, request.POST)
		
		if form.is_valid():
			# adds the new message to the Message database and redirects to the profile with a success message
			form.send(request)
			request.session['message'] = 'Message sent successfully!'
		
		return redirect('profile')
		
	message = 'Send a user a private message.'
	return render(request, 'compose_message.html', {'title': title, 'message': message, 'form': form})
	
# view for displaying messages sent to the user, simply passes all messages, including the usernames of the senders, to the template
@login_required	
def messages(request):
	username = request.user.username
	message_array = Message.objects.filter(to_user=User.objects.get(username=username))
	num_message = str(message_array.count())
	title = 'You have ' + num_message + ' messages!'
        
	return render(request, 'messages.html', {'username':username, 'title': title, 'message': message_array, 'num_message': num_message})
