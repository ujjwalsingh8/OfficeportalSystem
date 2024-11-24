from django.contrib import admin
from .models import Profile
# Register your models here.

@admin.register(Profile)
class Profileadmin(admin.ModelAdmin):
    list_display = ['id', 'role', 'is_approved']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Users have been approved.")
    approve_users.short_description = "Approve selected users"
