from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, OrganizationViewSet, ProjectViewSet, OrganizationUsersViewSet, WorkspaceViewSet, WorkspaceMembersViewSet, InviteMembers, OrganizationInvitedUserViewSet, FirstTimeUserAuth, UserWorkspaceRelationViewSet, UserProjectRelationViewSet, EventViewSet, WorkspaceEventViewSet, PostViewSet, WorkspacePostViewSet, ProjectPostViewSet, TaskViewSet, WorkspacePostCommentViewSet, ProjectPostCommentViewSet, UserProjectViewSet, UserTeamViewSet, TeamViewSet, ProjectEventViewSet, ProjectMembersViewSet, UserTeamRelationViewSet, TeamEventViewSet, TeamPostViewSet, TeamPostCommentViewSet, UserWorkspaceViewSet, MessageViewSet, LastMessageViewSet, ConversationViewSet
from django.contrib.auth.forms import UserCreationForm


router = routers.DefaultRouter()
router.register('users', UserViewSet, base_name='User')
router.register('organizations', OrganizationViewSet)
router.register('organization/members', OrganizationUsersViewSet)
router.register('organization/workspaces/posts', WorkspacePostViewSet)
router.register('organization/projects/posts', ProjectPostViewSet)
router.register('organization/teams/posts', TeamPostViewSet)
router.register('organization/workspaces/comments',
                WorkspacePostCommentViewSet)
router.register('organization/projects/comments',
                ProjectPostCommentViewSet)
router.register('organization/teams/comments',
                TeamPostCommentViewSet)
router.register('organization/workspaces/projects', ProjectViewSet)
router.register('organization/workspaces/teams', TeamViewSet)
router.register('organization/workspaces/tasks', TaskViewSet)
router.register('organization/users/workspaces', UserWorkspaceViewSet)
router.register('organization/users/projects', UserProjectViewSet)
router.register('organization/users/teams', UserTeamViewSet)
router.register('organization/users/conversations', ConversationViewSet)
router.register('organization/users/messages/last', LastMessageViewSet)
router.register('organization/users/messages', MessageViewSet)
router.register('organization/workspaces/members',
                WorkspaceMembersViewSet, base_name='workspace_members')
router.register('organization/projects/members',
                ProjectMembersViewSet, base_name='project_members')
router.register('organization/workspaces', WorkspaceViewSet)
# router.register('organization/projects', WorkspaceViewSet)
router.register('posts', PostViewSet)

router.register('organizations', OrganizationViewSet)
router.register('organization/events/workspace', WorkspaceEventViewSet)
router.register('organization/events/project', ProjectEventViewSet)
router.register('organization/events/team', TeamEventViewSet)
router.register('organization/events', EventViewSet)
router.register('organization/invites', OrganizationInvitedUserViewSet)
router.register('organization/workspace/add', UserWorkspaceRelationViewSet)
router.register('organization/project/add', UserProjectRelationViewSet)
router.register('organization/team/add', UserTeamRelationViewSet)

# router.register('users/auth', FirstTimeUserAuth)
# router.register('invite', InviteMembers, basename='Invite')

urlpatterns = [
    path('', include(router.urls)),
    path('invite', InviteMembers.as_view()),
    path('authenticate', FirstTimeUserAuth.as_view())
]
