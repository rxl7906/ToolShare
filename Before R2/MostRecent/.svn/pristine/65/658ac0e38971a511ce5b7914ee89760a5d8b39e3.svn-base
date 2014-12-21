from django.contrib.auth.models import User
from django import forms
from communities.models import Community, Review
from tools.models import Tool
from users.models import UserProfile

# form for the moderator to remove a tool from the community toolshed
class RemoveToolForm(forms.Form):
	def __init__(self, request, *args, **kwargs):
		super(RemoveToolForm, self).__init__(*args,**kwargs)
		community = UserProfile.objects.get(user=User.objects.get(username=request.user.username)).community
		self.fields['name'] = forms.ModelChoiceField(Tool.objects.filter(community=community, available=True), label='Tool', required=True)
	
	# removes a tool by setting its available flag to false	
	def remove_tool(self, request):
		name = self.cleaned_data.get('name')
		tool = Tool.objects.get(name=name)
		tool.available = False
		tool.save()

# form for the moderator to remove (ban) a user		
class RemoveUserForm(forms.Form):
	def __init__(self, request, *args, **kwargs):
		super(RemoveUserForm, self).__init__(*args,**kwargs)
		community = UserProfile.objects.get(user=User.objects.get(username=request.user.username)).community
		self.fields['name'] = forms.ModelChoiceField(UserProfile.objects.filter(community=community, user__is_active=True).exclude(user__username=request.user.username), label='Tool', required=True)
	
	# removes a user by setting the is_active flag to false	
	def remove_user(self, request):
		name = self.cleaned_data.get('name')
		user = User.objects.get(username=name)
		user.is_active = False
		user.save()
	
# form for a user to submit a review on another user	
class ReviewForm(forms.Form):
	def __init__(self, request, *args, **kwargs):
		super(ReviewForm, self).__init__(*args, **kwargs)
		user = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
		self.fields['username'] = forms.ModelChoiceField(UserProfile.objects.filter(community=user.community, user__is_active=True), label='For', required=True)
		self.fields['stars'] = forms.ChoiceField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], required=True)
		self.fields['review'] = forms.CharField(widget=forms.Textarea, label='Review', required=True)

	# saves a review to the Review model
	def post(self, request):
		username = self.cleaned_data.get('username')
		stars = self.cleaned_data.get('stars')
		review = self.cleaned_data.get('review')
		for_user = User.objects.get(username=username)
		by_user = User.objects.get(username=request.user.username)
		community = UserProfile.objects.get(user=User.objects.get(username=for_user.username)).community
		Review.post(review, for_user, by_user, stars, community)
