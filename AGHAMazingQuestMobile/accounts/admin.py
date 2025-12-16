from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import User
from .models import EmailOTP


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
	model = User
	fieldsets = DefaultUserAdmin.fieldsets + (
		("Additional", {"fields": ("display_name", "scores", "avatar")} ),
	)
	list_display = ("username", "display_name", "email", "is_staff", "scores")


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
	list_display = ("email", "code", "used", "created_at", "expires_at")
	list_filter = ("used",)
	search_fields = ("email",)
