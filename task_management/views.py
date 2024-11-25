from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from task_management.models import Task
from task_management.forms import TaskForm
from user_managment.models import Profile
# Create your views here.

#-----Task Management------

@login_required(login_url='login')
def manager_task(request):
    if request.user.is_superuser or request.user.main_user.role == 'Manager':
        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.assigned_by = request.user
                task.save()
                return redirect('manager_home')  
        else:
            form = TaskForm() 
        return render(request, 'task.html', {'form': form})
    else:
        return redirect('login')
    

#------------------Task Review-------------------

@login_required(login_url='login')
def task_view(request):   
    tasks = Task.objects.filter(assigned_to=request.user)
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        status = request.POST.get('status')
        comment = request.POST.get('comment')
        task = Task.objects.get(id=task_id)

        if task.status != 'Completed':
            task.status = status
            task.comment = comment  
            task.save()

        return redirect('employees_home')
    return render(request, 'task_view.html', {'tasks': tasks})


#-------------------Manager View Task Process------

@login_required(login_url='login')
def manager_view(request):
    if request.user.is_superuser or request.user.main_user.role == 'Manager':
        tasks = Task.objects.filter(assigned_by=request.user)

        return render(request, 'manager_task_view.html', {'tasks': tasks})
    else:
        return redirect('login')
