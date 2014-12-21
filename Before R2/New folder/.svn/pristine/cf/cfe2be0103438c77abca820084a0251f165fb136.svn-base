from django.contrib.auth.models import User
from django.db import IntegrityError
from django import forms
from users import fields
from users.models import UserProfile, Message
from communities.models import Community
from django.contrib.auth import authenticate, login

# form for creating a new user
class SignUpForm(forms.Form):
	first_name = forms.CharField(max_length=50, label='First Name', required=True)
	last_name = forms.CharField(max_length=50, label='Last Name', required=True)
	email = forms.CharField(max_length=50, label='Email', required=False)
	username = forms.CharField(max_length=50, label='Username', required=True)
	password = forms.CharField(widget=forms.PasswordInput, max_length=50, label='Password', required=True)
	confirm_password = forms.CharField(widget=forms.PasswordInput, max_length=50, label='Confirm Password', required=True)
	zip_code = forms.CharField(max_length=5, min_length=5, label='Zip Code', required=True)
	pickup_arrangement = forms.CharField(widget=forms.Textarea, label='Pickup Arrangement', required=False)
	
	# gathers the new user information and pass them to the model for creating a new user
	def save(self):
		new_user_info = {}
		new_user_info['first_name'] = self.cleaned_data.get('first_name')
		new_user_info['last_name'] = self.cleaned_data.get('last_name')
		new_user_info['email'] = self.cleaned_data.get('email')
		new_user_info['username'] = self.cleaned_data.get('username')
		new_user_info['password'] = self.cleaned_data.get('password')
		confirm_password = self.cleaned_data.get('confirm_password')
		new_user_info['zip_code'] = self.cleaned_data.get('zip_code')
		new_user_info['pickup_arrangement'] = self.cleaned_data.get('pickup_arrangement')
		
		# if the passwords do not match, throw a ValidationError exception
		if new_user_info['password'] != confirm_password:
			raise forms.ValidationError('The passwords do not match.')
		
		# if the zip code entered is not numeral, throw a ValidationError exception	
		if not new_user_info['zip_code'].isdigit():
			raise forms.ValidationError('A zip code cannot contain non-numbers.')
		
		# creates the new user and returns the username and password for authentication		
		UserProfile.add_user(new_user_info)
		return new_user_info['username'], new_user_info['password']

# form to create or join a community
class JoinCommunityForm(forms.Form):
	def __init__(self, request, *args, **kwargs):
		super(JoinCommunityForm, self).__init__(*args, **kwargs)
		user = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
		self.fields['community'] = fields.CommunityModelChoiceField(Community.objects.filter(zip_code=user.zip_code), label='Community', required=False)
		self.fields['new_community'] = forms.CharField(max_length=50, label='Or name of a new community', required=False)
	
	# sets the community for the user
	def set(self, request):
		community = self.cleaned_data.get('community')
		new_community = self.cleaned_data.get('new_community')
		user = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
		
		# determines if the user wants to create a new community or join an existing one
		if new_community == '':
			user.join_community(community)
		else:
			user.join_community(new_community)
			
# form for signing in an user
class SignInForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'id': 'username', 'placeholder': 'Username', 'class':'form-control'}), max_length=50, label='Username', required=True)
	password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'inputPassword', 'placeholder': 'Password', 'class':'form-control'}), max_length=50, label='Password', required=True)
	
	# returns the username and password for authentication
	def get(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		
		return username, password

# form to change the user's name						
class ChangeNameForm(forms.Form):
	first_name = forms.CharField(max_length=50, label='First Name', required=True)
	last_name = forms.CharField(max_length=50, label='Last Name', required=True)
	
	# changes the user's first and last name
	def change_name(self, request):
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		
		request.user.first_name = first_name
		request.user.last_name = last_name
		request.user.save()

# form for changing the user's zip code		
class ChangeZipCodeForm(forms.Form):
	zip_code = forms.CharField(max_length=5, min_length=5, label='Zip Code', required=True)
	
	# changes the user's zip code
	def change_zip_code(self, request):
		zip_code = self.cleaned_data.get('zip_code')
		
		# if the zip code is not numeral, throw a ValidationError exception
		if not zip_code.isdigit():
			raise forms.ValidationError('A zip code cannot contain non-numbers.')
		
		user_profile = UserProfile.objects.get(user=request.user)
		user_profile.zip_code = zip_code
		user_profile.save()

# form for updating the user's pickup arrangement	
class UpdatePickupArrangementForm(forms.Form):
	pickup_arrangement = forms.CharField(widget=forms.Textarea, label='Pickup Arrangement')
	
	# updates the user's pickup arrangement
	def change_pickup_arrangement(self, request):
		pickup_arrangement = self.cleaned_data.get('pickup_arrangement')
		
		user_profile = UserProfile.objects.get(user=request.user)
		user_profile.pickup_arrangement = pickup_arrangement
		user_profile.save()
	
# form for updating the user's password
class ChangePasswordForm(forms.Form):
	current_password = forms.CharField(widget=forms.PasswordInput, max_length=50, label='Current Password', required=True)
	new_password = forms.CharField(widget=forms.PasswordInput, max_length=50, label='New Password', required=True)
	confirm_new_password = forms.CharField(widget=forms.PasswordInput, max_length=50, label='Confirm New Password', required=True)
	
	# returns the current and new password for authentication
	def get(self, request):
		current_password = self.cleaned_data.get('current_password')
		new_password = self.cleaned_data.get('new_password')
		confirm_new_password = self.cleaned_data.get('confirm_new_password')
		
		# if the passwords do not match, throw a ValidationError exception
		if new_password != confirm_new_password:
			raise forms.ValidationError('The passwords do not match.')
		
		return current_password, new_password

# form to delete a user's account
class DeleteAccountForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput, max_length=50, label='Current Password', required=True)
	delete = forms.BooleanField(label="Are you sure you want to delete your account? This cannot be undone.")
	
	# the checkbox is required, so if it is not checked, nothing happens. If it is, return the password for authentication
	def get(self):
		password = self.cleaned_data.get('password')
		delete = self.cleaned_data.get('delete_account')
		
		return password

# form for composing a message			
class MessageForm(forms.Form):
	def __init__(self, request, *args, **kwargs):
		super(MessageForm, self).__init__(*args, **kwargs)
		user = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
		self.fields['username'] = forms.ModelChoiceField(UserProfile.objects.filter(zip_code=user.zip_code), label='To', required=True)
		self.fields['message'] = forms.CharField(widget=forms.Textarea, label='Message', required=True)
	
	# sends a message -- actually just saves it to the Message model
	def send(self, request):
		username = self.cleaned_data.get('username')
		message = self.cleaned_data.get('message')
		to_user = User.objects.get(username=username)
		from_user = User.objects.get(username=request.user.username)
		Message.send(message, from_user, to_user)
