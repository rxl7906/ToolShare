from django.test import TestCase
from communities.models import *
from users.models import *

"""
ReviewTestCase unit tests:
	- posting reviews for another user
"""
class ReviewTestCase(TestCase):
	def test_create_review(self):
			#Create two users
			UserProfile.add_user( {'first_name': "Devin" , 'last_name':"Sherman" , \
				'username': "devin" , 'email': "devin@example.com" , \
				'password': "sherman" , 'zip_code': 12345 , 'pickup_arrangement' : "RIT"})

			UserProfile.add_user( {'first_name': "Joe" , 'last_name':"Repass" , \
				'username': "joe" , 'email': "joe@example.com" , \
				'password': "repass" , 'zip_code': 12345 , 'pickup_arrangement' : "RIT"})

			user1 = User.objects.get(username="devin")  
			user2 = User.objects.get(username="joe")

			user1_reviews = Review.objects.filter(by_user=user1)
			user2_reviews = Review.objects.filter(for_user=user2)

			self.assertEqual(len(user1_reviews), 0)
			self.assertEqual(len(user2_reviews), 0)

			#Create Community

			Comm = Community.objects.create(name = "New Community", moderator = "devin", zip_code = 12345)

			#Post the reviewdef post(review, for_user, by_user, stars, community):
			Review.post("Joe took very good care of the tools I loaned to him.", user2, user1, 4, Comm)

			user1_reviews = Review.objects.filter(by_user=user1)
			user2_reviews = Review.objects.filter(for_user=user2)

			self.assertEqual(len(user1_reviews), 1)
			self.assertEqual(len(user2_reviews), 1)

			self.assertEqual(user1_reviews[0],user2_reviews[0])
			self.assertEqual(user1_reviews[0].review, "Joe took very good care of the tools I loaned to him.")
			self.assertEqual(user2_reviews[0].review, "Joe took very good care of the tools I loaned to him.")