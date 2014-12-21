from django.contrib.auth.models import User
from django.db import models
from communities.models import Community

# Extends the authentication User model with additional user attributes
class UserProfile(models.Model):
	user = models.OneToOneField(User)
	community = models.ForeignKey(Community, to_field='name', related_name='+', null=True, blank=True)
	zip_code = models.CharField(max_length=5)
	pickup_arrangement = models.CharField(max_length=200)
	borrow_count = models.IntegerField(default=0)
	loan_count = models.IntegerField(default=0)
	
	# add a new user to the database
	def add_user(new_user_info):
		user = User.objects.create_user(new_user_info['username'], new_user_info['email'], new_user_info['password'])
		user.first_name = new_user_info['first_name']
		user.last_name = new_user_info['last_name']
		user.save()
		
		user_profile = UserProfile(
			user=user,
			zip_code=new_user_info['zip_code'],
			pickup_arrangement=new_user_info['pickup_arrangement'],
		)
		
		user_profile.save()
	
	# adds an user to a community
	def join_community(self, community_name):
		# if the community already exists, join it
		try:
			community = Community.objects.get(name=community_name)
		# if not, create a new one
		except Community.DoesNotExist:
			new_community = Community(name=community_name, moderator=self.user.username, zip_code=self.zip_code)
			new_community.save()
			community = Community.objects.get(name=community_name)
		
		self.community = community
		self.save()
	
	# gets a user's information in a dictionary				
	def get_profile_info(self):
		user_info = {}
		user_info['First Name'] = str(self.user.first_name)
		user_info['Last Name'] = str(self.user.last_name)
		user_info['Email'] = str(self.user.email)
		user_info['Zip Code'] = str(self.zip_code)
		user_info['Pickup Arrangement'] = str(self.pickup_arrangement)
		
		return user_info
			
	def __str__(self):
		return self.user.username

# messages between users	
class Message(models.Model):
	message = models.CharField(max_length=200)
	from_user = models.ForeignKey(User, to_field='username', related_name='+')
	to_user = models.ForeignKey(User, to_field='username', related_name='+')
	
	# adds a new message
	def send(message, from_user, to_user):
		new_message = Message(message=message, from_user=from_user, to_user=to_user)
		new_message.save()
			
	def __str__(self):
		return self.from_user.username + ': ' + self.message
