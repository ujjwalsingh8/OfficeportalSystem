from django.urls import path
from leave_management import views


urlpatterns = [
    path('leave-application/', views.leave_applications, name='leave'),
    path('manager-leave/', views.manager_leave_applications, name='manager_leave_applications'),
    path('manager/<int:id>/<str:status>/', views.update_leave, name='update_leave_status'),
    path('leave-status/', views.employee_leave, name='leavestatus'),
    path('daily-status/', views.daily_status, name='daily_status'),
    path('daily-status-view/', views.daily_status_view, name='daily_status_view'),
    path('check-in/', views.check_in, name='check_in'),
    path('check-out/', views.check_out, name='check_out'),
]