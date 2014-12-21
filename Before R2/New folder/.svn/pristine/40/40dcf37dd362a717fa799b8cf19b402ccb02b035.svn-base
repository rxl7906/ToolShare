from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg

# model to contain attributes of a community
class Community(models.Model):
	name = models.CharField(max_length=50, unique=True)
	moderator = models.CharField(max_length=20)
	zip_code = models.CharField(max_length=5)
	
	# gets a formatted string containing the community rating for the join community form
	def get_rating_str(self):
		ratings = Rating.objects.filter(community=self)
		if ratings.exists():
			return str(self.name) + ' -- Rating: ' + str(ratings.aggregate(Avg('rating'))['rating__avg'])
		else:
			return str(self.name) + ' -- Rating: No ratings yet'
			
	def get_rating(self):
		ratings = Rating.objects.filter(community=self)
		if ratings.exists():
			return str(ratings.aggregate(Avg('rating'))['rating__avg'])
		else:
			return 'No ratings yet'
	
	def __str__(self):
		return self.name

# model to hold the individual ratings for the communities
class Rating(models.Model):
	community = models.ForeignKey(Community, to_field='name', related_name='+')
	rating = models.IntegerField(max_length=1)
	
	# saves a rating to the database
	def add_rating(community, rating):
		new_rating = Rating(community=community, rating=rating)
		new_rating.save()
		
	def __str__(self):
		return self.community.name + " " + self.rating

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