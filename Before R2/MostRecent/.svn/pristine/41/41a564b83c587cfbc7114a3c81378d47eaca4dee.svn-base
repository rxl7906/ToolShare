from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.contrib.auth.models import User
from tools import forms
from tools.models import Tool

# view to add a new tool
@login_required
def add_tool(request):
	title = 'Add a tool to your toolshed!'
	
	if request.method == 'GET':
		form = forms.AddToolForm()
	else:
		form = forms.AddToolForm(request.POST)
	
		if form.is_valid():
			# saves the tool to the Tool model
			try:
				form.save(request)
			except ValidationError as e:
				message = e.message
				return render(request, 'form.html', {'title': title, 'message': message, 'form': form})
				
			# if successful, redirect to the user's toolshed with a success message				
			request.session['message'] = 'Tool successfully added!'
			return redirect('my_toolshed')
	
	message = 'Fill in the information below to add a tool!'
	return render(request, 'add_tool.html', {'title': title, 'message': message, 'form': form})
	
# view to delete a tool
@login_required
def delete_tool(request):
	title = 'Delete a tool!'
	
	if request.method == 'GET':
		form = forms.DeleteToolForm(request)
	else:
		form = forms.DeleteToolForm(request, request.POST)
		
		if form.is_valid():
			# removes the tool from the Tool model
			form.delete()
			
			# if successful, redirect to the user's toolshed with a success message				
			request.session['message'] = 'Tool successfully deleted!'
			return redirect('my_toolshed')
			
	message = 'Choose a tool to remove from your toolshed.'									
	return render(request, 'delete_tool.html', {'title': title, 'message': message, 'form': form})
	
# view to submit a request to borrow a tool
@login_required
def borrow_tool(request):
	title = 'Borrow a tool!'
	
	if request.method == 'GET':
		form = forms.BorrowToolForm(request)
	else:
		form = forms.BorrowToolForm(request, request.POST)
		
		if form.is_valid():
			# submits a request to borrow this tool
			form.borrow(request)
			
			# if successful, redirect to the user's toolshed with a success message				
			request.session['message'] = 'You have successfully sent a request to borrow a tool!'
			return redirect('my_toolshed')
			
	message = 'Choose a tool you would like to borrow!'
	return render(request, 'borrow_tool.html', {'title': title, 'message': message, 'form': form})

# view to approve a borrow request
@login_required
def approve_request(request):
	title = 'Approve a Request!'
	
	if request.method == 'GET':
		form = forms.ApproveRequestForm(request)
	else:
		form = forms.ApproveRequestForm(request, request.POST)
		
		if form.is_valid():
			# approves the request for this tool
			form.mark_as_approved(request)
			
			
			# if successful, redirect to the user's toolshed with a success message				
			request.session['message'] = 'Request successfully approved!'
			return redirect('my_toolshed')
			
	message = 'Choose a borrow request to approve.'									
	return render(request, 'approve_request.html', {'title': title, 'message': message, 'form': form})

# view to reject a borrow request
@login_required
def reject_request(request):
	title = 'Reject a Request!'
	
	if request.method == 'GET':
		form = forms.RejectRequestForm(request)
	else:
		form = forms.RejectRequestForm(request, request.POST)
		
		if form.is_valid():
			# reject this borrow request
			form.mark_as_rejected(request)
			
			# if successful, redirect to the user's toolshed with a success message				
			request.session['message'] = 'Request successfully rejected!'
			return redirect('my_toolshed')
			
	message = 'Choose a borrow request to reject.'									
	return render(request, 'reject_request.html', {'title': title, 'message': message, 'form': form})

# view to allow the owner to mark a tool as returned
@login_required
def return_tool(request):
	title = 'Mark tool as returned!'
	
	if request.method == 'GET':
		form = forms.ReturnToolForm(request)
	else:
		form = forms.ReturnToolForm(request, request.POST)
		
		if form.is_valid():
			# mark this tool as returned
			form.mark_as_returned(request)
		
			# if successful, redirect to the user's toolshed with a success message				
			request.session['message'] = 'Tool successfully marked as returned!'
			return redirect('my_toolshed')
			
	message = 'Choose a tool to mark as returned.'									
	return render(request, 'mark_tool_returned.html', {'title': title, 'message': message, 'form': form})

# view to allow the owner to move the tool to the community toolshed
@login_required
def make_available(request):
	title = 'Move a tool to the community toolshed!'
	
	if request.method == 'GET':
		form = forms.MakeAvailableForm(request)
	else:
		form = forms.MakeAvailableForm(request, request.POST)
		
		if form.is_valid():
			# make this tool available for loan
			form.make_available(request)
			
			# if successful, redirect to the user's toolshed with a success message				
			request.session['message'] = 'You have successfully moved a tool to the community toolshed!'
			return redirect('my_toolshed')
			
	message = 'Choose a tool you would like to move to the community toolshed!'
	return render(request, 'make_available.html', {'title': title, 'message': message, 'form': form})

# view to allow the owner to move a tool out of the community toolshed
@login_required
def make_unavailable(request):
	title = 'Move a tool out of the community toolshed!'
	
	if request.method == 'GET':
		form = forms.MakeUnavailableForm(request)
	else:
		form = forms.MakeUnavailableForm(request, request.POST)
		
		if form.is_valid():
			# moves this tool out of the community toolshed
			form.make_unavailable(request)
			
			# if successful, redirect to the user's toolshed with a success message				
			request.session['message'] = 'You have successfully moved a tool out of the community toolshed!'
			return redirect('my_toolshed')
			
	message = 'Choose a tool you would like to move out of the community toolshed!'
	return render(request, 'make_unavailable.html', {'title': title, 'message': message, 'form': form})
