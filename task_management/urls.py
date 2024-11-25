from django.urls import path
from task_management import views

urlpatterns = [
    path('manager-task/', views.manager_task, name='manager_task'),
    path('task-view/', views.task_view, name='task_view'),
    path('manager-view/', views.manager_view, name='manager_view'),
]