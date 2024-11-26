from django.urls import path
from . import views

urlpatterns = [
    path('view_salary_pdf/<int:id>/', views.generate_salary_pdf, name='view_salary_pdf'),

]