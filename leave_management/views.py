from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from leave_management.models import LeaveAppication
from leave_management.forms import LeaveApplicationsForm
# Create your views here.

#--------------emaployees leave----------

@login_required(login_url='login')
def leave_applications(request):
    """this function is use for employee leave"""

    if request.user.main_user.role == 'Employees':  
        if request.method == 'POST':
            data = LeaveApplicationsForm(request.POST)
            if data.is_valid():
                leave_application = data.save(commit=False)
                leave_application.user = request.user
                leave_application.save()
                messages.success(request, "Leave application submitted successfully!")
                return redirect('employees_home')
        else:
            data = LeaveApplicationsForm()
        return render(request, 'leave.html', {'form': data})
    else:
        return redirect('login')
    
#-----------leave status-------

@login_required(login_url='login')
def employee_leave(request):
    """Employee can see leave status"""

    if request.user.main_user.role == 'Employees': 
            leaves = LeaveAppication.objects.filter(user=request.user)  
            return render(request, 'employee_leave_history.html', {'leave': leaves})
    else:
        return redirect('login')


#------------leave manager approve---------

@login_required(login_url='login')
def manager_leave_applications(request):
    '''Manager can approve or reject leave application'''

    if request.user.is_superuser or request.user.main_user.role == 'Manager':
            pending_leaves = LeaveAppication.objects.filter(leave_status='Pending')
            pending = pending_leaves.count()
            return render(request, 'manager_leave_applications.html', {'pending_leaves': pending_leaves, 'pending':pending})
    else:
        return redirect('login')

#---------leave status---------

@login_required(login_url='login')
def update_leave(request, id, status):
    """Updates the status of a leave application. 
    It allows the manager to approve or reject leave applications with a 'Pending' status.
    """
    if request.user.is_superuser or request.user.main_user.role == 'Manager':
        leave_application = get_object_or_404(LeaveAppication, pk=id)
        
        if leave_application.leave_status == 'Pending':
            if status == 'approve':
                leave_application.leave_status = 'Approved'
                leave_application.approved_by = request.user
                leave_application.save()
                messages.success(request, "Leave has been approved.")
                
                send_leave_email(leave_application, 'approved')

            elif status == 'reject':
                leave_application.leave_status = 'Rejected'
                leave_application.approved_by = request.user
                leave_application.save()
                messages.success(request, "Leave has been rejected.")
                
                send_leave_email(leave_application, 'rejected')

            return redirect('manager_leave_applications')
        
        else:
            messages.error(request, "This leave application has been processed.")
            return redirect('manager_leave_applications')
    else:
        return redirect('login')

#------send email------
def send_leave_email(leave_application, status):
    subject = f"Your Leave Application has been {status}"
    message = f"Hello {leave_application.user.username},Your leave application from {leave_application.start_date} to {leave_application.end_date} has been {status}.Thank you,Your Company"
    send_mail(subject, message, 'thecode8228@gmail.com', {leave_application.user.email},)