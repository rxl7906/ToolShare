from django.contrib.auth.models import User
from django.db import models
from communities.models import Community

class Tool(models.Model):
	name = models.CharField(max_length=50, unique=True)
	type = models.CharField(max_length=50)
	note = models.CharField(max_length=50)
	community = models.ForeignKey(Community, to_field='name', related_name='+')
	owner = models.ForeignKey(User, to_field='username', related_name='+')
	borrower = models.ForeignKey(User, to_field='username', related_name='+', null=True, default=None)
	approved = models.BooleanField(default=False)
	available = models.BooleanField(default=False)
	borrow_count = models.IntegerField(default=0)
	uniqueId = models.AutoField(primary_key=True)
	
	# adds a new tool to this model
	def add_tool(tool_info, available, community, owner):
		tool = Tool(
			name=tool_info['name'],
			type=tool_info['type'],
			note=tool_info['note'],
			available=available,
			community=community,
			owner=owner
		)
		tool.save()

	# turns the available flag to true
	def make_available(tool):
		tool.availability = True
		tool.save()
	
	# turns the available flag to false
	def make_unavailable(tool):
		tool.availability = False
		tool.save()
	
	# returns a cleaned up string for requests
	def get_requestor(self):
		return str(self.name) + " -- requested by " + str(self.borrower)
		
	def __str__(self):
		return self.name