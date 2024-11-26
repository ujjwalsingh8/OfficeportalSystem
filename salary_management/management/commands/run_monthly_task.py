# your_app/management/commands/run_monthly_task.py
# new line
from django.core.management.base import BaseCommand
from datetime import datetime

from django.contrib.auth.models import  User

from salary_management.views import generate_salary_pdf

class Command(BaseCommand):
    help = 'Runs a task on the 5th of each month'

    def handle(self, *args, **kwargs):
        # Ensure the task runs only on the 5th of the month
        today = datetime.today()
        if today.day == 25:
            self.stdout.write(self.style.SUCCESS('Running task for the 5th of the month...'))
            self.run_monthly_task()
        else:
            self.stdout.write(self.style.SUCCESS(f"Today is {today.strftime('%Y-%m-%d')}, not the 5th of the month. Task skipped."))

    def run_monthly_task(self):
        all_users = User.objects.filter(main_user__isnull=False).distinct()
        for user in all_users:
            generate_salary_pdf(user)
