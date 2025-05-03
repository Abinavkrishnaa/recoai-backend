from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Content,UserInteraction

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Profile', {'fields': ('display_name', 'bio', 'avatar', 'date_of_birth', 'location', 'interests')}),
        ('App Info', {'fields': ('is_premium', 'onboarding_complete', 'last_active', 'metadata')}),
        ('Notifications', {'fields': ('email_notifications', 'push_notifications')}),
        ('Social', {'fields': ('followers',)}),
    )
    filter_horizontal = ('followers',)
admin.site.register(Content)
admin.site.register(UserInteraction)