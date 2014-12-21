from django.test import TestCase
from tools.models import *
from users.models import *

"""
ToolsTestCase unit tests:
	- creating a tool and making sure it exists in the database
	- making a tool unavailable
"""
class ToolsTestCase(TestCase):
	"""
	This tests the add tool functionality, verifying that the tool is in the database.
	"""
	def test_add_tool(self):
		#Create User
		UserProfile.add_user( {'first_name': "Nick" , 'last_name':"Flumerfeldt" , \
			'username': "nick" , 'email': "nick@example.com" , \
			'password': "flum" , 'zip_code': 12345 , 'pickup_arrangement' : "RIT"})
		nick = User.objects.get(username="nick")
		self.assertEqual(nick.username, "nick")
		
		#Create Community
		Comm = Community.objects.create(name = "New Community", moderator = "nick", zip_code = 12345)
		
		#Add Tool
		tool_info = {'name' : "Drill", 'type' : "Power Tool", 'note': "None"}
		
		Tool.add_tool(tool_info, False, Comm, nick)

		addedTool = Tool.objects.get(name="Drill")
		self.assertEqual(addedTool.name, "Drill")
		

	"""
	This tests the functionality to make a tool unavailable, verifying that the tool is unavailable.
	"""
	def test_make_tool_unavailable(self):
		#Create User
		UserProfile.add_user( {'first_name': "Ryan" , 'last_name':"Zarchy" , \
			'username': "ryan" , 'email': "admin@example.com" , \
			'password': "zarchy" , 'zip_code': 12345 , 'pickup_arrangement' : "RIT"})
		ryan = User.objects.get(username="ryan")
		self.assertEqual(ryan.username, "ryan")
		
		#Create Community
		Comm = Community.objects.create(name = "New Community", moderator = "ryan", zip_code = 12345)
		
		#Add Tool
		tool_info = {'name' : "Drill", 'type' : "Power Tool", 'note': "None"}
		
		Tool.add_tool(tool_info, False, Comm, ryan)

		addedTool = Tool.objects.get(name="Drill")
		self.assertEqual(addedTool.name, "Drill")
		
		Tool.make_unavailable(addedTool)
		self.assertEqual(addedTool.available, False)
	
	
	