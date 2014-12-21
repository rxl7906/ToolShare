from django.test import TestCase
from users.models import *
# Create your tests here.

"""
UserTestCase unit tests:
	- creating a user (making sure they exist in the database)
	- messaging between two users
"""
class UserTestCase(TestCase):
	"""
	This tests the functionality of creating a user, verifying that they exist 
	in the database after creation.
	"""
	def test_create_user(self):
		#Create User
		UserProfile.add_user( {'first_name': "Robin" , 'last_name':"Li" , \
			'username': "robin3" , 'email': "admin@example.com" , \
			'password': "li" , 'zip_code': 12345 , 'pickup_arrangement' : "RIT"})

		#Verify user was created and exists in the database.
		robin = User.objects.get(username="robin3")
		self.assertEqual(robin.username, "robin3")


	"""
	This tests the functionality of sending a message from one user to another,
	verifying that each user is linked to the same message object, thus verifying 
	that the message has been sent.
	"""
	def test_create_message(self):
		#Create two users
		UserProfile.add_user( {'first_name': "Erika" , 'last_name':"Zuniga" , \
			'username': "erika" , 'email': "admin@example.com" , \
			'password': "zuniga" , 'zip_code': 12345 , 'pickup_arrangement' : "RIT"})

		UserProfile.add_user( {'first_name': "Brian" , 'last_name':"To" , \
			'username': "brian" , 'email': "admin@example.com" , \
			'password': "to" , 'zip_code': 12345 , 'pickup_arrangement' : "RIT"})

		#Assign users
		user1 = User.objects.get(username="erika")
		user2 = User.objects.get(username="brian")

		user1_messages = Message.objects.filter(from_user=user1)
		user2_messages = Message.objects.filter(to_user=user2)

		#Verify no messages have been sent to or from each user.
		self.assertEqual(len(user1_messages), 0)
		self.assertEqual(len(user2_messages), 0)

		#Send the message from erika to brian.
		Message.send("hey", user1, user2)

		user1_messages = Message.objects.filter(from_user=user1)
		user2_messages = Message.objects.filter(to_user=user2)

		#Verify that user 1 sent a message and user 2 received the message.
		self.assertEqual(len(user1_messages), 1)
		self.assertEqual(len(user2_messages), 1)

		#Verify the two users are linked to the same message object
		self.assertEqual(user1_messages[0],user2_messages[0])