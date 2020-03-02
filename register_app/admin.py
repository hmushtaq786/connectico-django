from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _
from .models import User, Organization, Workspace, Project, Team, Task, Event, WorkspaceEvent, ProjectEvent, TeamEvent, Role, user_workspace_relation, user_project_relation, user_team_relation, Post, WorkspacePost, ProjectPost, TeamPost, Notification, Comment,  Message, InvitedUser
# Register your models here.

UserAdmin.add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('first_name', 'last_name', 'username', 'email', 'password1', 'password2',
                   'organization_id', 'is_staff',
                   'is_superuser', 'status_line', 'photo_address', 'phone_number', 'groups', 'user_permissions'),
    }),
)

# UserAdmin.fieldsets = (None, {'fields': ('email', 'password')}),

UserAdmin.fieldsets += ('Details',
                        {'fields': ('organization_id', 'status_line', 'photo_address', 'phone_number',
                                    'is_first_login')}),

UserAdmin.list_display = (
    'username', 'email', 'first_name', 'last_name', 'is_staff')
admin.site.register(User, UserAdmin)
admin.site.register(Organization)
admin.site.register(Workspace)
admin.site.register(Project)
admin.site.register(Team)
admin.site.register(Task)
admin.site.register(Event)
admin.site.register(WorkspaceEvent)
admin.site.register(ProjectEvent)
admin.site.register(TeamEvent)
admin.site.register(Role)
admin.site.register(user_workspace_relation)
admin.site.register(user_project_relation)
admin.site.register(user_team_relation)
admin.site.register(Post)
admin.site.register(WorkspacePost)
admin.site.register(ProjectPost)
admin.site.register(TeamPost)
admin.site.register(Notification)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(InvitedUser)
