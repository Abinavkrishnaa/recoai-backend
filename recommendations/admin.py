from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User,Content,UserInteraction

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass
admin.site.register(Content)
admin.site.register(UserInteraction)