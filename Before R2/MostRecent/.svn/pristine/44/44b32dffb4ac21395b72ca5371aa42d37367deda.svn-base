from django.contrib.auth.models import User
from django import forms
from tools.models import Tool
from tools import fields
from users.models import UserProfile, Message

# form to add a new tool to the Tool model
class AddToolForm(forms.Form):
	name = forms.CharField(max_length=50, label='Tool Name', required=True)
	kind = forms.CharField(max_length=50, label='Tool Type', required=True)
	note = forms.CharField(max_length=50, label='Note', required=False)
	available = forms.BooleanField(initial=True, required=False)
	
	# gathers the input and creates a new tool in the Tool model
	def save(self, request):
		tool_info = {}
		tool_info['name'] = self.cleaned_data.get('name')
		tool_info['type'] = self.cleaned_data.get('kind')
		tool_info['note'] = self.cleaned_data.get('note')
		available = self.cleaned_data.get('available')
		owner = User.objects.get(username=request.user.username)
		community = UserProfile.objects.get(user=owner).community
		Tool.add_tool(tool_info, available, community, owner)

# form to delete a tool from the Tool model		
class DeleteToolForm(forms.Form):
	def __init__(self, request, *args, **kwargs):
		super(DeleteToolForm, self).__init__(*args,**kwargs)
		self.fields['name'] = forms.ModelChoiceField(Tool.objects.filter(owner=User.objects.get(username=request.user.username, borrower=None)), label='Tool To Delete')
		
	# deletes a tool from the Tool model
	def delete(self):
		name = self.cleaned_data.get('name')
		tool = Tool.objects.get(name=name)
		tool.delete()

# form to submit a borrow request for a tool
class BorrowToolForm(forms.Form):
	def __init__(self, request, *args, **kwargs):
		super(BorrowToolForm, self).__init__(*args,**kwargs)
		user = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
		self.fields['name'] = forms.ModelChoiceField(Tool.objects.exclude(owner=request.user.username).filter(community=user.community, borrower=None), label='Tool to Borrow')
	
	# submits a request to borrow a tool by setting the borrower attribute in the model, but leaving the approved flag to false
	def borrow(self, request):
		name = self.cleaned_data.get('name')
		tool = Tool.objects.get(name=name)
		borrower = User.objects.get(username=request.user.username)
		tool.borrower = borrower
		tool.approved = False
		tool.available = False
		tool.save()

# form to approve a borrow request		
class ApproveRequestForm(forms.Form):
	def __init__(self, request, *args, **kwargs):
		super(ApproveRequestForm, self).__init__(*args,**kwargs)
		user = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
		self.fields['name'] = fields.RequestModelChoiceField(Tool.objects.exclude(borrower=None).filter(owner=request.user.username, community=user.community, approved=False), label='Request to Approve')		

	# mark as approved by setting the approved flag to true
	def mark_as_approved(self, request):
		name = self.cleaned_data.get('name')
		tool = Tool.objects.get(name=name)
		
		message = "Your request to borrow " + str(tool) + " from " + request.user.username + " has been approved."
		from_user = User.objects.get(username=request.user.username)
		to_user = tool.borrower
		
		tool.approved = True
		tool.borrow_count += 1		# increments the times the tool was borrowed
		owner = UserProfile.objects.get(user=tool.owner)
		borrower = UserProfile.objects.get(user=tool.borrower)
		owner.loan_count += 1		# increments the times the owner has loaned a tool
		borrower.borrow_count += 1	# increments the times the borrowered has borrowed a tool
		tool.save()
		owner.save()
		borrower.save()
		Message.send(message, from_user, to_user)
	
# form to reject a borrow request	
class RejectRequestForm(forms.Form):
	def __init__(self, request, *args, **kwargs):
		super(RejectRequestForm, self).__init__(*args,**kwargs)
		user = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
		self.fields['name'] = fields.RequestModelChoiceField(Tool.objects.exclude(borrower=None).filter(owner=request.user.username, community=user.community, approved=False), label='Request to Reject')		
	
	# marks the request as rejected by setting the borrower attribute to None and leaving the approved flag as false
	def mark_as_rejected(self, request):
		name = self.cleaned_data.get('name')
		tool = Tool.objects.get(name=name)
		
		message = "Your request to borrow " + str(tool) + " from " + request.user.username + " has been rejected."
		from_user = User.objects.get(username=request.user.username)
		to_user = tool.borrower
		
		tool.borrower = None
		tool.approved = False
		tool.available = True
		tool.save()
		Message.send(message, from_user, to_user)
		
# form to mark a tool as returned
class ReturnToolForm(forms.Form):
	def __init__(self, request, *args, **kwargs):
		super(ReturnToolForm, self).__init__(*args,**kwargs)
		user = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
		self.fields['name'] = forms.ModelChoiceField(Tool.objects.exclude(borrower=None).filter(owner=request.user.username, community=user.community), label='Tool to Mark as Returned')
	
	# mark a tool as returned by setting the borrower to None and resetting the approved flag to false
	def mark_as_returned(self, request):
		name = self.cleaned_data.get('name')
		tool = Tool.objects.get(name=name)
		
		message = request.user.username + " have marked " + str(tool) + " as having been returned. The return process has been completed! Thank you for using ToolShare!"
		from_user = User.objects.get(username=request.user.username)
		to_user = tool.borrower
		
		name = self.cleaned_data.get('name')
		tool = Tool.objects.get(name=name)
		tool.borrower = None
		tool.approved = False
		tool.available = True
		tool.save()
		Message.send(message, from_user, to_user)

# view to move a tool to the community toolshed		
class MakeAvailableForm(forms.Form):
	def __init__(self, request, *args, **kwargs):
		super(MakeAvailableForm, self).__init__(*args,**kwargs)
		self.fields['name'] = forms.ModelChoiceField(Tool.objects.filter(owner=request.user.username, available=False), label='Tool', required=True)
		
	# makes the tool visible in the community toolshed by setting the available flag to true
	def make_available(self, request):
		name = self.cleaned_data.get('name')
		tool = Tool.objects.get(name=name)
		tool.available = True
		tool.save()
	
# form to move a tool out of the community toolshed
class MakeUnavailableForm(forms.Form):
	def __init__(self, request, *args, **kwargs):
		super(MakeUnavailableForm, self).__init__(*args,**kwargs)
		self.fields['name'] = forms.ModelChoiceField(Tool.objects.filter(owner=request.user.username, borrower=None, available=True), label='Tool', required=True)
		
	# moves a tool out of the community toolshed by setting the available flag to false	
	def make_unavailable(self, request):
		name = self.cleaned_data.get('name')
		tool = Tool.objects.get(name=name)
		tool.available = False
		tool.save()