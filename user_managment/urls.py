from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
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
    path('profile-update/', views.update_image, name='update_profile'),

]
