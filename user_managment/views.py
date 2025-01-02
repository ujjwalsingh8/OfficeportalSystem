from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from leave_management.models import CheckInCheckOut
from .forms import SignUpForm, ProfileUpdateForm, ProfileUpdate
# Create your views here.

def home(request):
    """Home page"""
    return render(request, 'base.html')

def signUp(request):
    """This function use for resiter Manager or Employees """
    if not request.user.is_authenticated:
        if request.method == 'POST':
            data = SignUpForm(request.POST)
            if data.is_valid():
                user = data.save()
                role = data.cleaned_data['role']
                Profile.objects.create(user = user, role=role, is_approved=False)
                messages.success(request, "User created successfully!")
                return redirect('login')
        else:
            data = SignUpForm()
        return render(request, 'signup.html', {'form':data})
    else:
        return redirect('login')

@login_required(login_url='login')
def admin_approval(request):
    """View for admin to approve users"""
    if request.user.is_superuser:
        unapproved_users = Profile.objects.filter(is_approved=False)

        if request.method == 'POST':
            user_ids = request.POST.get('approve')
            Profile.objects.filter(id__in=user_ids).update(is_approved=True)
            messages.success(request, "User have been approved.")

        return render(request, 'admin_approval.html', {'users': unapproved_users})

    return redirect('login')


def sign_in(request):
    """This function is only for login"""
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                passw = form.cleaned_data['password']

                user = User.objects.get(username=username) 
                user = authenticate(username=username, password=passw)
                if user is not None:
                    if user.is_superuser:
                        login(request, user)
                        messages.success(request, "Admin login successful!")
                        return redirect('admin_home')  

                    elif not user.main_user.is_approved:
                        messages.warning(request, "Your account is pending approval from an admin.")
                        return redirect('login') 

                    login(request, user)
                    messages.success(request, "Login successful!")
                    return redirect_user(user)
                
                else:
                    messages.error(request, "Incorrect password. Please try again.")             
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form':form})
    else:
        return redirect_user(request.user)

def redirect_user(user):
    '''This function is use for redirect user'''
    if user.is_superuser:
        return redirect('admin_home')
    if user.main_user.role == 'Manager':
        return redirect('manager_home')
    if user.main_user.role == 'Employees':
        return redirect('employees_home')


#------------Logout-------
def logout_user(request):
    logout(request)
    return redirect('/')


#--------------admin page-----------------

@login_required(login_url='login')
def admin_home(request):
    """The function is only for Admin"""

    if request.user.is_superuser:
        search_query = request.GET.get('search', '')

        if search_query:
            data1 = Profile.objects.filter(
                Q(user__username__icontains=search_query) |
                Q(user__email__icontains=search_query) |
                Q(role__icontains=search_query)
            ).order_by('id')
        else:
            data1 = Profile.objects.all().order_by('id')

        manager = []
        users = []

        for user in data1:
            if user.role == "Manager":
                manager.append(user.user)
            elif user.role == 'Employees':
                users.append(user.user)

        pagination = Paginator(users, 6, orphans=1)
        page_number = request.GET.get('page')
        page_obj = pagination.get_page(page_number)

        return render(request, 'admin_page.html', {'manager_list': manager, 'employees': page_obj, 'search_query': search_query})
    
    else:
        return redirect('login')

#--------manager admin -------------
@login_required(login_url='login')
def manager_home(request):
    """
    This function is only for Manager page
    """
    if request.user.main_user.role == 'Manager':
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        main_id = user
        ip = request.session.get('ip', 0)
        user_check_in = CheckInCheckOut.objects.filter(user=request.user, check_out_time__isnull=True).exists()

        return render(request, 'manager_home.html', {'profile': profile, 'user_check_in': user_check_in, 'main_id':main_id, 'ip':ip})
    else:
        return redirect('login')
    

#----------employee home---------
@login_required(login_url='login') 
def employees_home(request):
    '''
    This function is only for employees page
    '''
    if request.user.main_user.role == 'Employees':
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        main_id = user
        ip = request.session.get('ip', 0)
        
        user_check_in = CheckInCheckOut.objects.filter(user=request.user, check_out_time__isnull=True).exists()
        return render(request, 'employees_home.html', {'profile': profile, 'user_check_in': user_check_in, 'main_id':main_id, 'ip':ip})

    else:
        return redirect('login')


#------------update----------------

@login_required(login_url='login')
def update_profile(request, id):
    """
    This function is use for emaployee or manager update,
    Only can access Admin
    """
    if request.user.is_superuser:
        profile_obj = Profile.objects.get(user__id=id)
        if request.method == 'POST':
            data = ProfileUpdateForm(request.POST, instance=profile_obj)
            if data.is_valid():
                data.save()
                return redirect('admin_home')
        else:
            data = ProfileUpdateForm(instance=profile_obj)
        return render(request, 'update.html', {'form':data})
    else:
        return redirect('login')
    

#----------image update--------

@login_required(login_url='login')
def update_image(request, id):
    profile = get_object_or_404(Profile, pk=id)
    if request.method == 'POST':
        form = ProfileUpdate(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = ProfileUpdate(instance=profile)
    return render(request, 'update_profile.html', {'form': form})


#-------------delete----------

@login_required(login_url='login')
def delete_data(request, id):
    """This function is use for emaployee or manager detele,
    Only access Admin"""

    profile = get_object_or_404(User, pk=id)
    if request.method == 'POST':
        profile.delete() 
        return redirect('admin_home')
    return render(request, 'delete.html', {'profile': profile})


#-------
@login_required(login_url='login')
def change_pass(request):
    """Change Password with this Function"""
 
    if request.method == 'POST':
        data = PasswordChangeForm(user=request.user, data=request.POST)
        if data.is_valid():
            data.save()
            update_session_auth_hash(request, data.user)
            messages.success(request, "Password Changed Successfully!")  
        return redirect('login') 

    else:
        data = PasswordChangeForm(user=request.user)
    return render(request, 'changepass.html', {'form':data})

