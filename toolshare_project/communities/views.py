from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max, Avg
from users.models import UserProfile
from tools.models import Tool
from communities.models import Community, Review
from communities import forms

# the main view of the community, lists all the members and a link to review a user
@login_required
def main(request):
	username = request.user.username
	user = User.objects.get(username=username)
	community = UserProfile.objects.get(user=user).community
	user_array = UserProfile.objects.filter(community=community, user__is_active=True)
	
	return render(request, 'main.html', { 'community': str(community), 'user_array': user_array })

# view for the moderator, contains links to remove a user or a tool, and to view the statistics
@login_required
def admin(request):
	try:
		community = Community.objects.get(moderator=request.user.username)
	except Community.DoesNotExist:
		return redirect('main')
		
	reviews = Review.objects.filter(community=community)
	reviews_avg = reviews.aggregate(Avg('stars'))['stars__avg']
		
	return render(request, 'admin.html', {'reviews_avg': reviews_avg})
	
# statistics view to view most popular tools, most active users and number of tools and users in the community
@login_required
def statistics(request):
	user = User.objects.get(username=request.user.username)
	community = UserProfile.objects.get(user=user).community
	member_array = UserProfile.objects.filter(community=community)
	# the number of members in the community
	members = str(member_array.count())
	tool_array = Tool.objects.filter(community=community, available=True)
	# the number of tools available in the community
	tools = str(tool_array.count())
	# the highest borrow count by an user in the community
	borrow_count = member_array.aggregate(Max('borrow_count'))['borrow_count__max']
	# the highest loan count by an user in the community
	loan_count = member_array.aggregate(Max('loan_count'))['loan_count__max']
	# the username of the user with the highest borrow count
	borrower = UserProfile.objects.filter(borrow_count=borrow_count)[:1].get()
	# the username of the user with the highest loan count
	loaner = UserProfile.objects.filter(loan_count=loan_count)[:1].get()
	# the borrow count of the most popular tool
	tool_borrow_count = tool_array.aggregate(Max('borrow_count'))['borrow_count__max']
	
	# the tool with the highest borrow count
	try:
		tool = Tool.objects.filter(borrow_count=tool_borrow_count)[:1].get()
	# handles an exception if no tool has been added to the community yet
	except Tool.DoesNotExist:
		tool = 'There are no tools in the community toolshed yet.'
		
	return render(request, 'statistics.html', {'member_array': member_array, 'members': members, 'tool_array': tool_array, 'tools': tools, 'borrower': borrower, 'borrow_count': borrow_count, 'loaner': loaner, 'loan_count': loan_count, 'tool': tool, 'tool_borrow_count': tool_borrow_count })

# allows the moderator to remove a tool
@login_required
def remove_tool(request):
	# ensures the logged user is the moderator of this community
	try:
		Community.objects.get(moderator=request.user.username)
	except Community.DoesNotExist:
		return redirect('main')
	
	title = 'Remove a tool from the community toolshed!'
	
	if request.method == 'GET':
		form = forms.RemoveToolForm(request)
	else:
		form = forms.RemoveToolForm(request, request.POST)
		
		if form.is_valid():
			# deletes this tool from the Tool model by setting the available flag to false
			form.remove_tool(request)
			
			# redirects to the main page with a success message
			request.session['message'] = 'You have successfully moved a tool out of the community toolshed!'
			return redirect('main')
			
	message = 'Choose a tool you would like to move out of the community toolshed!'
	return render(request, 'remove_tool.html', {'title': title, 'message': message, 'form': form})

# allows the moderator to remove (ban) a user
@login_required
def remove_user(request):
	try:
		Community.objects.get(moderator=request.user.username)
	except Community.DoesNotExist:
		return redirect('main')
	
	title = 'Remove a user from the community!'
	
	if request.method == 'GET':
		form = forms.RemoveUserForm(request)
	else:
		form = forms.RemoveUserForm(request, request.POST)
		
		if form.is_valid():
			# removes a user by setting the is_active flag to false
			form.remove_user(request)
			request.session['message'] = 'You have successfully removed a user out of the community!'
			
			# redirects to the main page with a success message
			return redirect('main')
			
	message = 'Choose a user you would like to remove from the community!'
	return render(request, 'remove_user.html', {'title': title, 'message': message, 'form': form})
	
# allows a user to post a review on another user
@login_required	
def post_review(request):
	title = 'Post a Review.'
	
	if request.method == 'GET':
		form = forms.ReviewForm(request)
	else:
		form = forms.ReviewForm(request, request.POST)
		
		if form.is_valid():
			# posts the review
			form.post(request)
			request.session['message'] = 'Review posted successfully!'
		
		# redirects to the user's toolshed page with a success message
		return redirect('my_toolshed')
		
	message = 'Post a review for a user.'
	return render(request, 'post_review.html', {'title': title, 'message': message, 'form': form})

# a simple view that displays all reviews submitted in the user's community	
@login_required	
def reviews(request):
	user = UserProfile.objects.get(user=User.objects.get(username=request.user.username))
	reviews = Review.objects.filter(community=user.community)
	title = 'The reviews posted by the members of this community:'
        
	return render(request, 'reviews.html', { 'user': user, 'title': title, 'reviews': reviews })
