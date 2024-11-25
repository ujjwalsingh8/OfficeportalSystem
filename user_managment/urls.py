from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='reset_pass/password_reset_form.html', success_url ='/password-reset/done/'), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_pass/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='reset_pass/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='reset_pass/password_reset_complete.html'), name='password_reset_complete'),
    path('signup/', views.signUp, name='signup'),
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
    path('profile-update/<int:id>', views.update_image, name='update_profile'),

]