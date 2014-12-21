from django.contrib.auth.models import User
from django.db import models

# model to contain attributes of a community
class Community(models.Model):
	name = models.CharField(max_length=50, unique=True)
	moderator = models.CharField(max_length=20)
	zip_code = models.CharField(max_length=5)
	
	def __str__(self):
		return self.name

# model to store all reviews submitted by users on other users
class Review(models.Model):
	review = models.CharField(max_length=200)
	for_user = models.ForeignKey(User, to_field='username', related_name='+')
	by_user = models.ForeignKey(User, to_field='username', related_name='+')
	stars = models.IntegerField(max_length=1)
	community = models.ForeignKey(Community, to_field='name', related_name='+')
	
	# saves a new review to the database
	def post(review, for_user, by_user, stars, community):
		new_review = Review(review=review, for_user=for_user, by_user=by_user, stars=stars, community=community)
		new_review.save()
			
	def __str__(self):
		return 'For: ' + self.for_user.username + " By: " + self.by_user.username