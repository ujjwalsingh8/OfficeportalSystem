from django.db.models import Q
from django.db.models import F, ExpressionWrapper, DurationField, Sum
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, HttpResponse
from django.utils import timezone
from .models import SalarySlips
from leave_management.models import CheckInCheckOut
from weasyprint import HTML
from django.template.loader import render_to_string
from user_managment.models import Profile
# Create your views here.


def calculate_salary(user):
    hourly_billing = user.main_user.calculate_on_hour_billing

    current_date = datetime.now()

    total_user_hour = CheckInCheckOut.objects.filter(
        user= user,
        check_in_time__gte = datetime(current_date.year, current_date.month-1, 1),
        check_out_time__lt = datetime(current_date.year, current_date.month, 1)
    )

    # Annotate the queryset with the duration difference (check_out_time - check_in_time)

    queryset = total_user_hour.annotate(
        worked_duration=ExpressionWrapper(
            F('check_out_time') - F('check_in_time'),
            output_field=DurationField()
        )
    )
    # Now, sum the total of the worked durations across the queryset

    total_worked_duration = queryset.aggregate(
        total_duration_sum=Sum('worked_duration')
    )
    total_duration_sum = total_worked_duration['total_duration_sum']

    if total_duration_sum:
        total_hour = (total_duration_sum.days * 8) + total_duration_sum.seconds / 3600
    else:

        total_hour=0
    total_salary_hour = total_hour * hourly_billing
    
    return total_salary_hour if total_salary_hour else 0


def generate_salary_pdf(user, id):
    user = User.objects.get(id=id)
    basic_salary = user.main_user.basic_salary
    calulated_salary = calculate_salary(user)
    # Example data for an employee (you can replace this with actual data from your database)
    employee = {
        'id': user.id,
        'name': user,
        'role': user.main_user.role,
        'basic_salary': basic_salary,
        'deduction': basic_salary-calulated_salary,
        'total_salary': calulated_salary
    }

    html_string = render_to_string('salary_slip_template.html', {'employee': employee})

    html = HTML(string=html_string)
    pdf = html.write_pdf()

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="salary_slip.pdf"'

    pdf_file = ContentFile(pdf)
    current_date = datetime.now()

    salary_slip = SalarySlips.objects.create(
        user = user,
        month_year = f'{current_date.month}-{current_date.year}',
        disbursed_salary = calulated_salary,
    )
    salary_slip.salary_pdf.save(f"salary_slip_{user.id}.pdf", pdf_file)
    
    subject = f"Your Salary Slip for {current_date.month}-{current_date.year}"

    message = f"{user.get_full_name()},\n\nPlease find attached your salary slip for the month {current_date.month}-{current_date.year}." 

    email = EmailMessage(
        subject=subject,
        body=message,
        from_email= settings.EMAIL_HOST_USER ,
        to=[user.email] 
    )
    
    email.attach(f"salary_slip_{user.id}.pdf", pdf, 'application/pdf')
    email.send()

    return response
   
