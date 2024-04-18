from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Team,Status,Priority,Task,Chat
from .forms import SignUpForm,EditUserProfileForm

class CustomUserAdmin(UserAdmin):
    add_form = SignUpForm
    form = EditUserProfileForm
    model = CustomUser
    list_display=['name','email','password']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'name')
    ordering = ('email',)
admin.site.register(CustomUser,CustomUserAdmin)       

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display=['team_members']

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display=['content']

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display=['task_status']

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display=['priority_status']

# @admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display=('id','team','task','owner','status','priority','notes','files')

admin.site.register(Task,TaskAdmin)