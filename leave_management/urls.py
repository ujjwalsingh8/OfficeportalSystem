from django.urls import path
from leave_management import views


urlpatterns = [
    path('leave-application/', views.leave_applications, name='leave'),
    path('manager-leave/', views.manager_leave_applications, name='manager_leave_applications'),
    path('manager/<int:id>/<str:status>/', views.update_leave, name='update_leave_status'),
    path('leave-status/', views.employee_leave, name='leavestatus'),
]