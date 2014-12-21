from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from users.models import UserProfile
from tools.models import Tool
from tools import forms


# displays all tools owned by the logged in user
@login_required
def my_toolshed(request):
	# several views redirect here -- display the relevant success message
	try:
		message = request.session['message']
		del request.session['message']
	# if there was no redirect, display a welcome message
	except KeyError:
		message = 'Welcome to your toolshed!'
	
	username = request.user.username
	# all tools owned by the user
	tools = Tool.objects.filter(owner=User.objects.get(username=username))
	# all tools that the owner has marked as available (visible in the community toolshed)
	available = tools.filter(available=True)
	# all tools that the owner has marked as unavailable (not visible in the community toolshed)
	not_available = tools.filter(available=False)
	# all tools that are currently being borrowed
	borrowed = tools.exclude(borrower=None).filter(approved=True)
	# all tools that the user is borrowing from others
	borrowing = Tool.objects.filter(borrower=username, approved=True)
	# all pending requests to borrow tools from the user
	incoming = tools.exclude(borrower=None).filter(approved=False)
	# all pending requests made by the user to borrow tools from others
	outgoing = Tool.objects.filter(borrower=username, approved=False)
	

	if request.method == "POST":
		for key in request.POST:
			if request.POST[key] == "Approve":
				tool = Tool.objects.get(uniqueId=int(key))
				tool.approved = True
				tool.borrow_count += 1      # increments the times the tool was borrowed
				owner = UserProfile.objects.get(user=tool.owner)
				borrower = UserProfile.objects.get(user=tool.borrower)
				owner.loan_count += 1       # increments the times the owner has loaned a tool
				borrower.borrow_count += 1  # increments the times the borrowered has borrowed a tool
				tool.save()
				owner.save()
				borrower.save()
				request.session['message'] = 'Request successfully approved!'
				return redirect('my_toolshed')
			elif request.POST[key] == "Deny":
				tool = Tool.objects.get(uniqueId=int(key))
				tool.borrower = None
				tool.approved = False
				tool.available = True
				tool.save()
				request.session['message'] = 'Request successfully rejected!'
				return redirect('my_toolshed')
			else:
				tool = Tool.objects.get(uniqueId=int(key))
				tool.borrower = None
				tool.approved = False
				tool.available = True
				tool.save()
				request.session['message'] = 'Tool successfully marked as returned!'
				return redirect('my_toolshed')

	return render(request, 'my_toolshed.html', { 'message': message, 'available': available, 'not_available': not_available, 'borrowed': borrowed, 'borrowing': borrowing, 'incoming': incoming, 'outgoing': outgoing })

# a simple view for the community toolshed which displays all tools whose owners belong to the community, and has its available flag set to true
@login_required
def community_toolshed(request):    
	username = request.user.username
	community = UserProfile.objects.get(user=User.objects.get(username=username)).community
	tools = Tool.objects.filter(community=community).filter(available=True)
	# print(request.POST)
	if request.method == 'GET':
		form = forms.BorrowToolForm(request)
	else:
		for key in request.POST:
			if request.POST[key] == "Borrow Tool":
				tool = Tool.objects.get(uniqueId=int(key))
				borrower = User.objects.get(username=request.user.username)
				tool.borrower = borrower
				tool.approved = False
				tool.available = False
				tool.save()
				form = forms.BorrowToolForm(request, request.POST)
				# if successful, redirect to the user's toolshed with a success message             
				request.session['message'] = 'You have successfully sent a request to borrow a tool!'
				return redirect('my_toolshed')

	return render(request, 'community_toolshed.html', { 'tools': tools, 'form': form })



	