from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.base, name='base'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='reset_pass/password_reset_form.html', success_url ='/password-reset/done/'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_pass/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='reset_pass/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_pass/password_reset_complete.html'), name='password_reset_complete'),
    path('signup/', views.sign_Up, name='signup'),
    path('admin-approval/', views.admin_approval, name='admin_approval'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('admin-home/', views.admin_home, name='admin_home'),
    path('manager-home/', views.manager_home, name='manager_home'),
    path('employees-home/', views.employees_home, name='employees_home'),
    path('update/<int:id>/', views.update_profile, name='update'),
    path('update-profile/', views.update_profile, name='update'),
    path('delete/<int:id>/', views.delete_data, name='delete'),
    path('change-password/', views.change_pass, name='chnagepass'),
    path('leave-application/', views.leave_applications, name='leave'),
    path('manager-leave/', views.manager_leave_applications, name='manager_leave_applications'),
    path('manager/<int:id>/<str:status>/', views.update_leave, name='update_leave_status'),
    path('leave-status/', views.employee_leave, name='leavestatus'),
    path('manager-task/', views.manager_task, name='manager_task'),
    path('task-view/', views.task_view, name='task_view'),
    path('manager-view/', views.manager_view, name='manager_view'),
    path('daily-status/', views.daily_status, name='daily_status'),
    path('daily-status-view/', views.daily_status_view, name='daily_status_view'),
    path('check-in/', views.check_in, name='check_in'),
    path('check-out/', views.check_out, name='check_out'),
    # path('salary-slip/<int:id>/', views.salary_slip, name='salary_slip'),
    path('profile-update/', views.update_image, name='update_profile'),
    # path('view_salary_pdf/<int:employee_id>/', views.generate_salary_pdf, name='view_salary_pdf'),

]